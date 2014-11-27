__author__ = 'qiang.he@chinache.com,xiaotian.wu@chinacache.com'

import smtplib
import sys
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

from config import config

class Notifier:
  def __init__(self):
    try:
      self.enablemail = config.get("mail", "enable")
      self.mailto = config.get("mail", "to")
      self.mailfrom = config.get("mail", "from")
      self.host = config.get("mail", "host")
      self.subject = config.get("mail", "subject")
      self.enablesms = config.get("sms", "enable")
      self.smslist = config.get("sms", "to").split(',')
    except Exception, exception:
      print exception

  def Send(self, content):
    if self.enablemail == 'true':
      self.SendMail(content)
    if self.enablesms == 'true':
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
