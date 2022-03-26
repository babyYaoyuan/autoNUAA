from email.mime.text import MIMEText
import smtplib
import time


def notify_email(text, subject):
    msg = MIMEText(text, 'plain', 'utf-8')

    email_address = '**@**.com'
    password = '**'

    msg['Subject'] = subject + ' ' + time.strftime("%H:%M:%S", time.localtime())
    msg['To'] = email_address
    msg['From'] = email_address

    server = smtplib.SMTP_SSL('smtp.**.com', 994)
    # debug level为1时，会输出log
    # server.set_debuglevel(1)
    server.login(email_address, password)
    server.sendmail(from_addr=email_address, to_addrs=[email_address], msg=msg.as_string())
    server.close()


if __name__ == '__main__':
    notify_email('test_context', 'test_subject')