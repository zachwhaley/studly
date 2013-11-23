#!/usr/bin/python
import smtplib
import subprocess
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# gather data from corosync resource manager monitor
task = subprocess.Popen("grep -R bitch /usr/src/*", shell=True, stdout=subprocess.PIPE)
data = task.stdout.read()
assert task.wait() == 0

# construct email headers and body  message
msg  = MIMEText("""This is a test failover notification from testNode1""")
sender = 'si2server@gmail.com'
recipients = ['trevor.latson@gmail.com' , 'trevor@si2.org' , '5123188212@vtext.com']
msg['Subject'] = "This is a SMTP test notification from Google's servers"
msg['From'] = sender
msg['To'] = ", ".join(recipients)

# log into google smtp server with TLS
session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
session.ehlo()
session.starttls()
session.ehlo()
session.login('<your_gmail_account>@gmail.com' , '<your password>')

# send message and data and log out
session.sendmail(sender, recipients, msg.as_string() + data )
session.quit()


