#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def mail_test():
    # me == my email address
    # you == recipient's email address
    me = "xiaofangliu@huashenghaoche.com"
    you = "xiaofangliu@huashenghaoche.com"
    pwd = "Asd..123"
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "test"
    msg['From'] = 'Shawna'
    msg['To'] = you
    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!/nHow are you?/nHere is the link you wanted:/nhttp://www.python.org"
    html = """/ 
    <html> 
      <head></head> 
      <body> 
        <p>Hi!<br> 
           How are you?<br> 
           Here is the <a href="http://www.python.org" mce_href="http://www.python.org">link</a> you wanted. 
        </p>
         <p>You Dear Shawna..</p>
      </body> 
    </html> 
    """
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    s.login(me, pwd)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()


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
    mail_test()