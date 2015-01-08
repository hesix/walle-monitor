__author__ = 'qiang.he@chinache.com,xiaotian.wu@chinacache.com'

import json
import logging
import logging.config
import os

logging_config_path = os.getenv('WALLE_MONITOR_PATH') + '/monitor/logging.conf'
message_schema_path = os.getenv('WALLE_MONITOR_PATH') + '/monitor/message_schema.json'

if not os.path.exists(logging_config_path):
  raise Exception("logging.conf doesn't exist under: %s" % logging_config_path)

if not os.path.exists(message_schema_path):
  raise Exception("message schema doesn't exist under: %s" % message_schema_path)

logging.config.fileConfig(logging_config_path)
logger = logging.getLogger("walle-monitor")

message_schema = ''
with open(message_schema_path) as f:
  message_schema = json.loads(f.read())
