__author__ = 'xiaotian.wu@chinacache.com'

from config import config, logger
from collector import ClientInfo

import MySQLdb

class HBaseExporter:
  def __init__(self):
    pass

  def Export(self, messages):
    pass

class MySQLExporter:

  def __init__(self):
    self._conn = MySQLdb.connect(
                   host = config.get("mysql", "host"),
                   port = config.getint("mysql", "port"),
                   user = config.get("mysql", "user"),
                   db = config.get("mysql", "db"))
    self._cursor = self._conn.cursor()
    self._table = config.get("mysql", "table")

  def __del__(self):
    self._cursor.close()
    self._conn.close()

  def Export(self, client_info_set):
    client_info_set = [(client_info.timestamp,
                        client_info.host,
                        client_info.server,
                        client_info.deposit_num,
                        client_info.msg_count,
                        client_info.msg_size,
                        client_info.total_msg_count,
                        1 if client_info.disconnect_count < 3 else 0)
                        for client_info in client_info_set]
    sql_insert = "insert into " + \
                  self._table + \
                 " values(%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
      self._cursor.executemany(sql_insert, client_info_set)
      self._conn.commit()
    except Exception, exception:
      logger.error(exception)

class CPickleExporter:
  def __init__(self):
    pass

  def Export(self, messages):
    pass

if __name__ == '__main__':
  exporter = MySQLExporter()
  client_info_set = []
  client_info = ClientInfo()
  client_info.timestamp = '20141126163600'
  client_info.host = 'MIS-BJ-6-5AI'
  client_info.server = 'MIS-BJ-6-5AI'
  client_info.deposit_num = 10
  client_info.msg_count = 100
  client_info.msg_size = 1000
  client_info.total_msg_count = 10000
  client_info.disconnect_count = 0
  client_info_set.append(client_info)
  exporter.Export(client_info_set)
