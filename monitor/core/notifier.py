__author__ = 'qiang.he@chinache.com,xiaotian.wu@chinacache.com'

import smtplib
import sys
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from monitor.core.options import parse_option

class Notifier:
  def __init__(self, options):
    self.mailto = options.mail_list.split(',')
    self.mailfrom = "qiang.he@chinacache.com"
    self.host = "corp.chinacache.com"
    self.smslist = options.sms_list.split(',')

  def Send(self, content, subject):
    if self.mailto != '':
      self.SendMail(content, subject)
    print self.smslist
    #if len(self.smslist) != 0:
    #  self.SendSMS(content)

  def SendMail(self, content, subject):
    msg = MIMEMultipart()
    msg['Subject'] = subject
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
  options = parse_option() 
  notifier = Notifier(options)
  notifier.SendMail("hello", "This is a test")
