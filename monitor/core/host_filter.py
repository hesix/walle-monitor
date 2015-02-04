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
      self.warning_host_list[host] += 1
      return False

  def DisconnectedHostJudger(self, host):
    if host not in self.disconnected_host_list.keys():
      self.disconnected_host_list[host] = 1
      return True
    else:
      self.disconnected_host_list[host] += 1
      return False

  def ResetFilter(self):
    max_warning = 0
    for host in self.warning_host_list.keys():
      max_warning = max(max_warning, self.warning_host_list[host])

    for host in self.warning_host_list.keys():
      if max_warning - self.warning_host_list[host] == 3:
        del self.warning_host_list[host]
      elif max_warning == 3:
        self.warning_host_list[host] = 0

    max_disconnected = 0
    for host in self.disconnected_host_list.keys():
       max_disconnected = max(max_disconnected, self.disconnected_host_list[host])

    for host in self.disconnected_host_list.keys():
      if max_disconnected - self.disconnected_host_list[host] == 3:
        del self.disconnected_host_list[host]
      elif max_disconnected == 3:
        self.disconnected_host_list[host] = 0

