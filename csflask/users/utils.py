from PIL import Image
import secrets
import os
from flask_mail import Message
from csflask import mail
from flask import url_for, current_app
from random import randint
import smtplib
from smtplib import SMTP as smtp
from email.mime.text import MIMEText as text
from decouple import config

def save_picture(form_picture):
    random_name = secrets.token_hex(8)
    _,file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_name + file_extension
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_filename)
    
    out_size = (300,200)
    i = Image.open(form_picture)
    i.thumbnail(out_size)
    i.save(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    body = (f""" Click the link below to reset your password:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request please ignore this message.
""")
    message = text(body)
    message['Subject'] = 'Password Reset Request'
    message['From'] = os.environ['GUNMAIL_EMAIL']
    message['To'] = user.email

    server = smtplib.SMTP('smtp.mailgun.com', 587)
    # server.starttls()
    server.login(os.environ['GUNMAIL_EMAIL'],os.environ['GUNMAIL_PASSWORD'])
    server.sendmail(os.environ['GUNMAIL_EMAIL'], user.email, message.as_string())
    server.quit()


def send_confirm_email(user):
    x = randint(10000,99999)
    body = f""" Your verification code is
{x}
Thank you for registering.

If you did not make this request please ignore this message.
"""
    message = text(body)
    message['Subject'] = 'Account confirmation code'
    message['From'] = os.environ['GUNMAIL_EMAIL']
    message['To'] = user

    server = smtplib.SMTP('smtp.mailgun.com', 587)
    # server.starttls()
    server.login(os.environ['GUNMAIL_EMAIL'],os.environ['GUNMAIL_PASSWORD'])
    server.sendmail(os.environ['GUNMAIL_EMAIL'], user, message.as_string())
    server.quit()

    return x

def send_reset_code(user):
    x = randint(10000,99999)
    body = f""" Your email reset code is
{x}

If you did not make this request please ignore this message.
"""
    message = text(body)
    message['Subject'] = 'Account confirmation code'
    message['From'] = 'emmanuel@email.mypass.icu'
    message['To'] = user

    server = smtplib.SMTP('smtp.mailgun.com', 587)
    # server.starttls()
    server.login(os.environ['GUNMAIL_EMAIL'],os.environ['GUNMAIL_PASSWORD'])
    server.sendmail(os.environ['GUNMAIL_EMAIL'], user, message.as_string())
    server.quit()

    return x 
