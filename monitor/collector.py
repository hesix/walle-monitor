__author__ = 'xiaotian.wu@chinacache.com'

import copy
import os
import logging

from config import config, logger, message_schema
                  
class ClientInfo:
  timestamp = None
  host = ''
  server = ''
  deposit_num = 0
  msg_count = 0
  msg_size = 0
  total_msg_count = 0
  disconnect_count = 0

class CustomErrorCollector:
  def __init__(self):
    self._file_deposit_allow = config.getint("behavior", "file_deposit_allow")
    self._disconnect_upper_bound = config.getint("behavior", "disconnect_upper_bound")
    self._pre_hosts = {}
    self._cur_hosts = {}
    self._message_schema = {}
    self._message_delimiter = message_schema["delimiter"]
    for item in message_schema["format"]:
      self._message_schema[item["name"]] = item["position"]
    self._timestamp_col = int(self._message_schema["timestamp"])
    self._host_col = int(self._message_schema["host"])
    self._server_col = int(self._message_schema["server"])
    self._deposit_col = int(self._message_schema["deposit"])
    self._msg_count_col = int(self._message_schema["msg_count"])
    self._msg_size_col = int(self._message_schema["msg_size"])
    self._total_msg_count_col = int(self._message_schema["total_msg_count"])

  def Collect(self, messages):
    warning_set = []
    connect_set = []
    for message in messages:
      if len(message) < 2 or len(message[1]) < 4:
        continue
      message = message[1][3].split(self._message_delimiter)
      ret, client_info = self.CollectWarning(message)
      if ret is True:
        warning_set.append(client_info)
      if client_info is not None:
        self._cur_hosts[client_info.host] = client_info
        connect_set.append(client_info)
    disconnect_set = self.CollectDisconnectedClient()
    self._pre_hosts = copy.deepcopy(self._cur_hosts)
    self._cur_hosts.clear()
    return (warning_set, disconnect_set, connect_set)

  def CheckWarning(self, client_info):
    if client_info.deposit_num >= self._file_deposit_allow:
      return True
    else:
      return False

  def CollectWarning(self, message):
    try:
      client_host = message[self._host_col]
      client_info = ClientInfo()
      client_info.timestamp = message[self._timestamp_col]
      client_info.host = message[self._host_col]
      client_info.server = message[self._server_col]
      client_info.deposit_num = int(message[self._deposit_col])
      client_info.msg_count = int(message[self._msg_count_col])
      client_info.msg_size = int(message[self._msg_size_col])
      client_info.total_msg_count = int(message[self._total_msg_count_col])
      client_info.disconnect_count = 0
      if self.CheckWarning(client_info) is True:
        logger.debug("client: %s has error, deposit num: %s" % (client_host, client_info.deposit_num))
        return True, client_info
      else:
        return False, client_info
    except Exception, exception:
      logger.warn(exception)
      return False, None

  def CollectDisconnectedClient(self):
    disconnect_set = []
    for client_host in self._pre_hosts.keys():
      client_info = self._pre_hosts[client_host]
      if client_host not in self._cur_hosts:
        client_info.disconnect_count += 1
        if client_info.disconnect_count >= self._disconnect_upper_bound:
          client_info.deposit_num = -1
          client_info.msg_count = -1
          client_info.msg_size = -1
          client_info.total_msg_count = -1
          disconnect_set.append(client_info)
      self._cur_hosts[client_host] = client_info
    return disconnect_set

if __name__ == '__main__':
  import unittest

  class CollectorTest(unittest.TestCase):
    def testCollectWarning(self):
      collector = CustomErrorCollector()
      message = "a\tb\tc\t0\t0\t0\t0".split('\t')
      ret, client_info = collector.CollectWarning(message)
      self.assertEqual(ret, False)
      message = "a\tb\tc\t11\t0\t0\t0".split('\t')
      ret, client_info = collector.CollectWarning(message)
      self.assertEqual(ret, True)

    def testCollectDisconnectedClient(self):
      collector = CustomErrorCollector()
      collector._pre_hosts["host1"] = ClientInfo()
      self.assertEqual(collector._pre_hosts["host1"].disconnect_count, 0)
      collector._cur_hosts = {}
      self.assertEqual(collector.CollectDisconnectedClient(), [])
      collector._pre_hosts["host1"].disconnect_count = 2
      collector._pre_hosts["host1"].host = "host1"
      collector._cur_hosts = {}
      disconnect_set = collector.CollectDisconnectedClient()
      self.assertEqual(disconnect_set[0].host, "host1")
      self.assertEqual(disconnect_set[0].deposit_num, -1)
      self.assertEqual(disconnect_set[0].msg_count, -1)
      self.assertEqual(disconnect_set[0].msg_size, -1)
      self.assertEqual(disconnect_set[0].total_msg_count, -1)

  def testCollect(self):
      #collector = CustomErrorCollector()
      #collector.Collect(messages):
      pass

  unittest.main()
