__author__ = 'xiaotian.wu@chinacache.com'

import json
import logging
import logging.config
import os

root_path = os.getenv('WALLE_MONITOR_PATH')
config_path = root_path + '/monitor/config'
logging_config_path = config_path + '/logging.conf'
message_schema_path = config_path + '/message_schema.json'
ipmap_path = config_path + '/ipmap.conf'

if not os.path.exists(logging_config_path):
  raise Exception("logging.conf doesn't exist under: %s" % logging_config_path)

if not os.path.exists(message_schema_path):
  raise Exception("message schema doesn't exist under: %s" % message_schema_path)

if not os.path.exists(ipmap_path):
  raise Exception("ipmap.config doesn't exist under: %s" % ipmap_path)

logging.config.fileConfig(logging_config_path)
logger = logging.getLogger("walle-monitor")

message_schema = ''
with open(message_schema_path) as f:
  message_schema = json.loads(f.read())
