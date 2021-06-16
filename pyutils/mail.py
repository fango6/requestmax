import smtplib
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formatdate


class MailSender(object):

    def __init__(self, user, password, smtp_host="smtp.qq.com", smtp_port=465):
        self.user = user
        self.password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send(self, subject, to_addrs, content):
        '''
        @params:
            subject: 邮件标题, str;
            to_addrs: 接受者的邮件地址, list;
            content: 发送邮件的内容, str.
        '''
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header(self.user, 'utf-8')
        msg['To'] = ', '.join(to_addrs)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        try:
            smtp_ssl = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            smtp_ssl.connect(self.smtp_host, self.smtp_port)
            smtp_ssl.login(self.user, self.password)
            smtp_ssl.sendmail(self.user, to_addrs, msg.as_string())
        except smtplib.SMTPException:
            traceback.print_exc()


if __name__ == "__main__":
    user = ''
    password = ''
    MailSender(user, password).send(
        '今天回家吃饭', ['fango6@qq.com'], '该说点什么呢?')
