#!/usr/bin/env python
# -*- coding:utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class SendMail(object):
    '''
    send mail helper
    '''

    def __init__(self, host, port, sender, senderName, useAuth, user, pwd, useSSL):
        self.host = host
        self.port = port
        self.sender = sender
        self.senderName = senderName
        self.useAuth = useAuth
        self.user = user
        self.password = pwd
        self.useSSL = useSSL

    def __format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self, mailtoList, subject, body):
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = self.__format_addr(self.user)
        msg['To'] = self.__format_addr(mailtoList)
        msg['Subject'] = Header(subject, 'utf-8').encode()
        server = smtplib.SMTP(str(self.host), str(self.port))
        server.set_debuglevel(1)
        server.login(self.user, self.password)
        server.sendmail(self.user, mailtoList, msg.as_string())
        server.quit()


def sendMailTest():
    def __format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    import traceback
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "654177962@qq.com"  # 用户名
    mail_pass = "xx"  # 口令

    sender = '654177962@qq.com'
    receivers = ['lglforfun@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('你好', 'plain', 'utf-8')
    message['From'] = "654177962@qq.com"
    message['To'] = "lglforfun@126.com"

    subject = '你好测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException, Exception:
        print traceback.print_exc()
        # print "Error: 无法发送邮件"


if __name__ == '__main__':
    # sm = SendMail(host="smtp.qq.com", port=25, sender="654177962@qq.com", senderName="lgl",
    #               useAuth=True, user="654177962@qq.com", pwd="xx", useSSL=True)
    # sm.send(mailtoList=["lglforfun@126.com"], subject="测试", body="测试body")

    sendMailTest()
