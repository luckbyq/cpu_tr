#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib,urllib2,time,datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#定义邮箱基本信息。
SMTPserver = 'smtp.mxhichina.com'
SMTPport = 25
sender = 'yaqi.bian@xqchuxing.com'
password = "Bianyaqi123456"
to = 'yaqi.bian@xqchuxing.com'

def mail(subject,message,enclosure):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #初始化根模块，定义为msg。
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject

    #定义附件。
    file = enclosure
    filepart = MIMEApplication(open(file,'rb').read())
    filepart.add_header('Content-Disposition','attachment',filename = file)

    #加载邮件模块中的文本信息，及附件信息。
    text = MIMEText(message + '\n' + nowTime)
    msg.attach(text)
    msg.attach((filepart))

    #发送邮件。
    try:
        mailserver = smtplib.SMTP(SMTPserver, SMTPport)
        mailserver.login(sender, password)
        mailserver.sendmail(sender, to, msg.as_string())
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


mail(subject = "This is a test subject for byq.", message = "if success.", enclosure = "E:\\test.txt")