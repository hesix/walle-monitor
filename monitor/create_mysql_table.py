__author__ = 'xiaotian.wu@chinacache.com'

import MySQLdb

if __name__ == '__main__':
  conn = MySQLdb.connect(host = '127.0.0.1',
                         port = 3306,
                         user = 'root',
                         db = 'walle',)
  cursor = conn.cursor()
  cursor.execute('create table test2(time_stamp timestamp(6), host varchar(15), kafka_server varchar(15), deposit_num int, msg_count int, msg_size int, total_msg_count int, online tinyint)')
  conn.commit()
  cursor.close()
  conn.close()
