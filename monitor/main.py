#!/usr/bin/python

__author__ = 'xiaotian.wu@chinacache.com'

import time

from config import config, logger
from collector import CustomErrorCollector
#from exporter import MySQLExporter
from fetcher import KafkaFetcher
#from notifier import Notifier

if __name__ == "__main__":
  fetcher = KafkaFetcher()
  fetch_interval = config.getint("kafka", "fetch_interval")
  custom_error_collector = CustomErrorCollector()
  #exporter = MySQLExporter()
  #notifier = Notifier()

  while True:
    logger.info("start fetching kafka messages...")
    monitor_messages = fetcher.Fetch()
    logger.info("start collecting data from fetched message set...")
    warning_set, disconnect_set, connect_set = custom_error_collector.Collect(monitor_messages)
    logger.debug("---------------------------warning set------------------------")
    for client in warning_set:
      logger.debug(client.host)
    logger.debug("---------------------------disconnect set---------------------")
    for client in disconnect_set:
      logger.debug(client.host)
    logger.debug("---------------------------connect set------------------------")
    for client in connect_set:
      logger.debug(client.host)
    #logger.info("append log to db...")
    #exporter.Export(disconnect_set + connect_set)
    #logger.info("send warningset/errorset notification...")
    #notifier.Send(str(warning_set))
    #notifier.Send(str(error_set))
    time.sleep(fetch_interval)
