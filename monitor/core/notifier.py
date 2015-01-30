__author__ = 'qiang.he@chinache.com,xiaotian.wu@chinacache.com'

import smtplib
import sys
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class Notifier:
  def __init__(options):
    self.mailto = options.mail_list
    self.mailfrom = "walle-monitor"
    self.host = options.mail_host
    self.subject = "log collector service warning"
    self.smslist = options.sms_list.split(',')

  def Send(self, content):
    if self.mailto != '':
      self.SendMail(content)
    if len(self.smslist) != 0:
      self.SendSMS(content)

  def SendMail(self, content):
    msg = MIMEMultipart()
    msg['Subject'] = self.subject
    msg['From'] = self.mailfrom
    msg['To'] = ";".join(self.mailto)
    try:
      msg.attach(MIMEText(content, 'plain', 'utf-8'))
      smtp = smtplib.SMTP(self.host)
      smtp.sendmail(self.mailfrom, self.mailto, msg.as_string())
      smtp.quit()
      return True
    except Exception, exception:
      print str(exception)
      return False

  def SendSMS(content):
    for user in self.smslist:
      os.system('/usr/qiang.he/send_sms %s "%s"' % (user, str(content)))

if __name__ == '__main__':
  notifier = Notifier()
  notifier.SendMail("hello")
