__author__ = 'xiaotian.wu@chinacache.com'

import threading

from monitor.config.config import logger, ipmap_path
from monitor.core.options import parse_option
from kafka import KafkaClient, MultiProcessConsumer, SimpleConsumer

class ConsumerInstance:
  def __init__(self, options):
    hosts = options.kafka_hosts
    consumer_group = options.consumer_group
    topic = options.topic
    consumer_type = options.consumer_type
    ipmap_file = ipmap_path if options.enable_kafka_ipmap else None
    self.client = KafkaClient(hosts, ip_mapping_file = ipmap_file)

    logger.info("kafka hosts: %s" % hosts)
    logger.info("consumer group: %s" % consumer_group)
    logger.info("topic: %s" % topic)
    logger.info("consumer type: %s" % consumer_type)
    logger.info("ip mapping file: %s" % ipmap_file)
   
    if consumer_type == "multiprocess":
      partitions_per_proc = options.partitions_per_proc
      partition_num = len(self.client.topic_partitions[topic])
      num_procs = partition_num * partitions_per_proc
      auto_commit_every_n = options.auto_commit_msg_count
      auto_commit_every_t = options.auto_commit_interval

      self.consumer = MultiProcessConsumer(
                        self.client,
                        consumer_group,
                        topic,
                        auto_commit_every_n,
                        auto_commit_every_t,
                        num_procs,
                        partitions_per_proc)

    elif consumer_type == "simple":
      self.consumer = SimpleConsumer(
                        self.client,
                        consumer_group,
                        topic,
                        False)
    else:
      raise Exception("unsuppported consumer type: %s" % typestr)

  def get(self):
    return self.consumer;

class KafkaFetcher:
  def __init__(self, options):
    self.consumer = ConsumerInstance(options)
    self.consumer.get().seek(0, 2)
    self.lock = threading.Lock()
    self.message_set_max_size = options.message_set_max_size
    self.fetch_timeout = options.fetch_timeout

  def fetch(self):
    self.lock.acquire()
    message_set = self.consumer.get().get_messages(
                    self.message_set_max_size,
                    False,
                    self.fetch_timeout)
    self.lock.release()
    return message_set

# for unit test
if __name__ == '__main__':
  options = parse_option()
  import time
  fetcher = KafkaFetcher(options)
  fetch_interval = options.fetch_interval
  while True:
    for message in fetcher.fetch():
      print message[1][3]
    time.sleep(fetch_interval)
