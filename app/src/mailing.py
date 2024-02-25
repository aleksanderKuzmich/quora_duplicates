import ssl
import smtplib
from email.mime.text import MIMEText


def send_mail(sender, recipient, password, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    ssl_context = ssl.create_default_context()
    port = 465
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl_context) as srv:
        srv.login("app.mailer.worker@gmail.com", password)
        srv.sendmail(sender, recipient, msg.as_string())
