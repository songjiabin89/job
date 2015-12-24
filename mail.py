#!/usr/bin/env python
#coding:utf-8
'''
Created on 2015年8月5日
@author: 宋家斌
'''

import smtplib  
from email.mime.text import MIMEText  # 引入smtplib和MIMEText
def sm(receiver, title, body):   #定义sm函数，并定义三个傎，此三个值分别是receiver：收件人地址， title：邮件抬头。 body：邮件内容。
        host = 'smtp.qq.com'   #发送邮箱SMTP服务器。
        port = 25       #端口号
        sender = '345278300@qq.com' #发送邮箱地址。
        pwd = '111111'   #发送邮箱密码。

        msg = MIMEText(body, 'html', 'utf-8')  #body:文件内容，html:文件格式，utf-8:指定文字编码。
        msg['subject'] = title
        msg['from'] = sender
        msg['to'] = receiver

        s = smtplib.SMTP(host, port) #连接邮箱。
        s.login(sender, pwd)    #登录账号密码
        s.sendmail(sender, receiver, msg.as_string())  #发送邮件。

        print 'The mail named %s to %s is sended successly.' % (title, receiver)
        
