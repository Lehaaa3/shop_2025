from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings


def send_mail_to_me(post_title):
    try:
        send_mail(
            subject='100 просмотров',
            message=f"Поздравляю, пост: '{post_title}' набрал 100 просмотров",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False
        )
    except SMTPException as error:
        print(error)


def send_mail_from_contact(name, phone, message):
    try:
        send_mail(
            subject=f'{name} - {phone}',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False
        )
    except SMTPException as error:
        print(error)
