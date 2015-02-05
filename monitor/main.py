#!/usr/bin/python

__author__ = 'xiaotian.wu@chinacache.com,qiang.he@chinacache.com'

import os
import socket
import time
import threading

from flask import Flask
from flask import render_template

from monitor.config.config import logger
from monitor.core.collector import CustomErrorCollector
from monitor.core.fetcher import KafkaFetcher
from monitor.core.options import parse_option
from monitor.core.host_filter import HostFilter 
from monitor.core.notifier import Notifier

app = Flask(__name__)
connect_set = None

@app.route('/deposit/')
def deposit():
  return render_template('deposit.html', clients = connect_set)

@app.route('/detail/')
def detail():
  return render_template('detail.html', clients = connect_set)

def start_web_service():
  def run():
    host = "0.0.0.0"
    port = 20000
    app.run(host = host, port = port)

  running_thread = threading.Thread(target = run)
  running_thread.start()

if __name__ == "__main__":
  options = parse_option()
  fetcher = KafkaFetcher(options)
  fetch_interval = options.fetch_interval
  custom_error_collector = CustomErrorCollector(options)
  start_web_service()
  host_filter = HostFilter()
  notifier = Notifier(options)
  
  while True:
    content = ""
    logger.info("start fetching kafka messages....")
    monitor_messages = fetcher.fetch()
    logger.info("start collecting data from fetched message set...")
    warning_set, disconnect_set, connect_set = custom_error_collector.Collect(monitor_messages)
    logger.debug("---------------------------warning set------------------------")
    for client in warning_set:
      logger.debug(client.host)
      if host_filter.WarningHostJudger(client.host):
        content += "%s\t\t%d\n" % (client.host, client.deposit_num)
    if content != "":
      content = "The clients' deposited file more than warning value\n%s" % content
      notifier.Send(content, "Accumulation Warning")
    content = ""
    logger.debug("---------------------------disconnect set---------------------")
    for client in disconnect_set:
      logger.debug(client.host)
      if host_filter.DisconnectedHostJudger(client):
        content += "%s\n" % client.host
    if content != "":
      content = "The clients' log_collector service have disconnected\n%s" % content
      notifier.Send(content, "log_collector Service Down")

    logger.debug("---------------------------connect set------------------------")
    for client in connect_set:
      logger.debug(client.host)
    
    host_filter.ResetFilter()
    time.sleep(fetch_interval)
