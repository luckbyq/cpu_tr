#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib,urllib2,time,datetime,sms
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


tosms = ''
for key in smsuser:
    if len(tosms) > 1:
        tosms = tosms + ',' + smsuser[key]
    else:
        tosms = tosms + smsuser[key]

def postsms(content):
    sms.post(content,tosms)


#主工作模块，发送邮件使用。
def mail(subject,message,enclosure):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #初始化根模块，定义为msg。
    msg = MIMEMultipart()
    msg['From'] = sender

    #多人群发时，直接在邮件发送代码中使用list即可。
    #msg['To'] = touser
    msg['Subject'] = subject

    #定义附件。
    file = enclosure
    filepart = MIMEApplication(open(file,'rb').read())
    filepart.add_header('Content-Disposition','attachment',filename = file)

    #加载邮件模块中的文本信息，及附件信息。
    text = MIMEText(message + '\n' + nowTime)
    msg.attach(text)
    msg.attach((filepart))

    #发送邮件。touser为多人邮件中的list。
    try:
        mailserver = smtplib.SMTP(SMTPserver, SMTPport)
        mailserver.login(sender, password)
        mailserver.sendmail(sender, touser, msg.as_string())
        mailserver.quit()
    except smtplib.SMTPRecipientsRefused:
        print 'Recipient refused'
    except smtplib.SMTPAuthenticationError:
        print 'Auth error'
    except smtplib.SMTPSenderRefused:
        print 'Sender refused'
    except smtplib.SMTPException, e:
        print e.message
    else:
        print "Sed mail Success!    %s" % nowTime

if __name__ == "__main__":
    # mail(subject = "This is a test subject for byq.", message = "if success.", enclosure = "E:\\test.txt")
    # postsms('This is the test message')
    pass
