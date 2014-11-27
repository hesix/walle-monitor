__author__ = 'qiang.he@chinache.com,xiaotian.wu@chinacache.com'

import ConfigParser
import json
import logging
import logging.config
import os

if not os.path.exists("logging.conf"):
  raise Exception("logging.conf doesn't exist")

if not os.path.exists("monitor.conf"):
  raise Exception("monitor.conf doesn't exist")

if not os.path.exists("message_schema.json"):
  raise Exception("message schema doesn't exist")

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("log")

config = ConfigParser.ConfigParser()
config.read("monitor.conf")

message_schema = ''
with open("message_schema.json") as f:
  message_schema = json.loads(f.read())
