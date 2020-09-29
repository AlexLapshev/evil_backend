import logging
import smtplib

from api.auth.secret import sender, sender_password
from api.auth.jwt_work import create_access_token

message = """From: From company <testfastapi@gmail.com>
To: To Person <{}>
Subject: [Evil Productions] Please confirm your email address

http://0.0.0.0:1984/api/v1/users/confirm/{}
"""

logger = logging.getLogger(__name__)


def connect_to_server() -> smtplib.SMTP:
    logging.debug('connecting to smpt server')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, sender_password)
    return server


def send_email_confirm(email: str) -> None:
    logging.debug('sending email')
    hashed_email = create_access_token({'email': email})
    server = connect_to_server()
    server.sendmail(sender, email, message.format(email, hashed_email))
    server.close()
