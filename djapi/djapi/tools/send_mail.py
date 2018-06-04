#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


class Mail(object):
    def __init__(self, title, sender, addressee, content, *args, **kwargs):
        self.send_smtp = settings.MAIL_INFO.get('send_smtp')
        self.smtp_port = settings.MAIL_INFO.get('smtp_port')
        self.send_account = settings.MAIL_INFO.get('send_account')
        self.send_pwd = settings.MAIL_INFO.get('send_pwd')
        self.title = title
        self.sender = sender
        self.addressee = addressee
        self.content = content
        print '++++++++++++++++++++++++'
        # print self.send_smtp, self.smtp_port, self.sender, self.addressee, self.send_pwd

    def _send(self):
        print 'this _send'
        res = True
        try:
            # print '======================'
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.title
            msg['From'] = self.sender
            msg['To'] = self.addressee
            print 'content', self.content
            main_body = MIMEText(self.content, 'html', 'utf-8')
            print 'msg', main_body
            msg.attach(main_body)

            # print 'msg', main_body
            server = smtplib.SMTP_SSL(self.send_smtp, self.smtp_port)
            server.login(self.send_account, self.send_pwd)
            # print 'server', server
            server.sendmail(self.send_account, self.addressee, msg.as_string())
            # print 'server1', server
            server.quit()
        except Exception:
            res = False
        print 'send_', res
        return res


if __name__ == '__main__':
    pass