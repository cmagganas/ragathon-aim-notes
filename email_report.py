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