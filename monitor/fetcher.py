__author__ = 'xiaotian.wu@chinacache.com'

from config import config
import threading

from kafka import KafkaClient, MultiProcessConsumer, SimpleConsumer

class ConsumerInstance:
  client = None
  consumer = None

  def __init__(self):
    global config
    try:
      hosts = config.get("kafka", "hosts")
      consumer_group = config.get("kafka", "consumer_group")
      topic = config.get("kafka", "topic")
      consumer_type = config.get("kafka", "consumer_type")
      self.client= KafkaClient(hosts)
    except Exception, exception:
      print exception

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
    self.lock = threading.Lock()

  def Fetch(self):
    self.lock.acquire()
    message_set = self.consumer.Get().get_messages(100, timeout = 5)
    self.lock.release()
    return message_set
    
# for unit test
if __name__ == '__main__':
  fetcher = KafkaFetcher()
  for message in fetcher.Fetch():
    print message[1][3]
