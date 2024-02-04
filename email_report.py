import os
import smtplib
from email.mime.text import MIMEText

SENDGRID_API_KEY = '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'

def send_email_report(subject, body, to_email):
    message = MIMEText(body)
    message['From'] = "meetingminutesai@gmail.com"
    message['To'] = to_email
    message['Subject'] = subject

    with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
        server.ehlo()
        server.starttls()
        server.login('apikey', SENDGRID_API_KEY)
        server.sendmail("meetingminutesai@gmail.com", [to_email], message.as_string())
