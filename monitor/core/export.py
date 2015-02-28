from influxdb import InfluxDBClient

class Exportor:
  def __init__(self, host):
     client = InfluxDBClient(host, 8086, 'root', 'root', 'walle_monitor')

  def export_detail(self, message):
    json_body = [{
      "points" : message,
      "name"   : "detail",
      "columns": ["timestamp", "host", "deposited", "speed", "size", "total"]
    }]
    self.client.write_points(json_body)

  def export_deposit(self, message):
    json_body = [{
      "points" : message,
      "name"   : "deposit",
      "columns": ["timestamp", "host", "deposited", "speed", "size", "total"]
    }]
    self.client.write_points(json_body)
    
