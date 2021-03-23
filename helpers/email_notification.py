import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import config


def send(msg_body: str):
    msg = MIMEMultipart() 

    msg['From'] = config.from_email
    msg['To'] = config.to_email

    msg['Subject'] = 'Nepremicnine Update'
    msg.attach(MIMEText(msg_body, 'plain')) 

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls() 

    s.login(msg['From'], config.gmail_api_key) 

    text = msg.as_string() 

    s.sendmail(msg['From'], msg['From'], text)
    s.quit()