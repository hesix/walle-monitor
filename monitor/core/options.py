__author__ = 'xiaotian.wu@chinacache.com'

from optparse import OptionParser

def parse_option():
  parser = OptionParser()
  parser.add_option("-a", "--kafka_hosts",
                    type = "string", dest = "kafka_hosts",
                    default = "", help = "kafka server hosts")
  parser.add_option("-b", "--consumer_group",
                    type = "string", dest = "consumer_group",
                    default = "walle-monitor-consumer", help = "kafka consumer group")
  parser.add_option("-c", "--topic",
                    type = "string", dest = "topic",
                    default = "zeus-log", help = "topic")
  parser.add_option("-d", "--consumer_type",
                    type = "string", dest = "consumer_type",
                    default = "simple", help = "consumer type")
  parser.add_option("-e", "--enable_kafka_ipmap",
                    action = "store_true", dest = "enable_kafka_ipmap",
                    default = True, help = "enable ip mapping")
  parser.add_option("-f", "--fetch_timeout",
                    type = "int", dest = "fetch_timeout",
                    default = 20, help = "fetch timeout")
  parser.add_option("-g", "--fetch_interval",
                    type = "int", dest = "fetch_interval",
                    default = 30, help = "fetch interval")
  parser.add_option("-i", "--message_set_max_size",
                    type = "int", dest = "message_set_max_size",
                    default = 20000, help = "message set max size")
  parser.add_option("-j", "--disconnect_upper_bound",
                    type = "int", dest = "disconnect_upper_bound",
                    default = 3, help = "consumer type")
  parser.add_option("-k", "--auto_commit_msg_count",
                    type = "int", dest = "auto_commit_msg_count",
                    default = 5000, help = "auto commit message count")
  parser.add_option("-l", "--auto_commit_interval",
                    type = "int", dest = "auto_commit_interval",
                    default = 30000, help = "auto commit interval")
  parser.add_option("-m", "--fetch_buffer_size_bytes",
                    type = "int", dest = "fetch_buffer_size_bytes",
                    default = 409600, help = "fetch buffer size")
  parser.add_option("-n", "--max_fetch_buffer_size_bytes",
                    type = "int", dest = "max_fetch_buffer_size_bytes",
                    default = 4096000, help = "max fetch buffer size")
  parser.add_option("-o", "--partitions_per_proc",
                    type = "int", dest = "partitions_per_proc",
                    default = 1, help = "partitions per proc")
  parser.add_option("-p", "--collect_time",
                    type = "int", dest = "collect_time",
                    default = 500000, help = "collect time")
  parser.add_option("-q", "--file_deposit_allow",
                    type = "int", dest = "file_deposit_allow",
                    default = 10, help = "file deposit allow count")
  parser.add_option("-r", "--sms_list",
                    type = "string", dest = "sms_list",
                    default = "", help = "sms to list")
  parser.add_option("-s", "--mail_list",
                    type = "string", dest = "mail_list",
                    default = "", help = "mail list")
  parser.add_option("-t", "--mail_host",
                    type = "string", dest = "mail_host",
                    default = "", help = "mail host")
  (options, args) = parser.parse_args()
  return options

