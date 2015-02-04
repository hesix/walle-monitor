__author__ = 'qiang.he@chinacache.com'

class HostFilter:
  def __init__(self):
    self.warning_host_list = {}
    self.disconnected_host_list = {}

  def WarningHostJudger(self, host):
    if host not in self.warning_host_list.keys():
      self.warning_host_list[host] = 1
      return True
    else:
      self.disconnected_host_list[host] = 1
      return False

  def DisconnectedHostJudger(self, host_list):
    if host not in self.disconnected_host_list.keys():
      self.disconnected_host_list[host] = 1
      return True
    else:
      self.disconnected_host_list[host] = 1
      return False

  def ResetFilter(self):
    for host in self.warning_host_list.keys():
      if self.warning_host_list[host] == 0:
        del self.warning_host_list[host]
      else:
        self.warning_host_list[host] = 0
  
    for host in self.disconnected_host_list.keys():
      if self.disconnected_host_list[host] == 0:
        del self.disconnected_host_list[host]
      else:
        self.disconnected_host_list[host] = 0

