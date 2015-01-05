__author__ = 'xiaotian.wu@chinacache.com'

import threading

from config import config, logger
from kafka import KafkaClient, MultiProcessConsumer, SimpleConsumer

class ConsumerInstance:
  client = None
  consumer = None

  def __init__(self):
    hosts = config.get("kafka", "hosts")
    consumer_group = config.get("kafka", "consumer_group")
    topic = config.get("kafka", "topic")
    consumer_type = config.get("kafka", "consumer_type")
    ip_mapping = config.get("kafka", "ip_mapping_file")
    logger.info("kafka hosts: %s" % hosts)
    logger.info("consumer group: %s" % consumer_group)
    logger.info("topic: %s" % topic)
    logger.info("consumer type: %s" % consumer_type)
    logger.info("ip mapping file: %s" % ip_mapping)
    self.client = KafkaClient(hosts, ip_mapping_file = ip_mapping)
    if consumer_type == "multiprocess":
      partitions_per_proc = config.getint("behavior", "partitions_per_proc")
      partition_num = len(self.client.topic_partitions[topic])
      num_procs = partition_num * partitions_per_proc
      auto_commit_every_n = config.getint("behavior", "auto_commit_msg_count")
      auto_commit_every_t = config.getint("behavior", "auto_commit_interval")
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

  def Get(self):
    return self.consumer;

class KafkaFetcher:
  def __init__(self):
    self.consumer = ConsumerInstance()
    self.consumer.Get().seek(0, 2)
    self.lock = threading.Lock()
    self.message_set_max_size = config.getint("kafka", "message_set_max_size")
    self.fetch_timeout = config.getint("kafka", "fetch_timeout")

  def Fetch(self):
    self.lock.acquire()
    message_set = self.consumer.Get().get_messages(
                    self.message_set_max_size,
                    False,
                    self.fetch_timeout)
    self.lock.release()
    return message_set
    
# for unit test
if __name__ == '__main__':
  import time
  fetcher = KafkaFetcher()
  fetch_interval = config.getint("kafka", "fetch_interval")
  while True:
    for message in fetcher.Fetch():
      print message[1][3]
    time.sleep(fetch_interval)
