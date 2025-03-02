from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings


def greeting_email(username, user_email):
    try:
        send_mail(
            subject='LehStore',
            message=f"Поздравляю, {username}, вы успешно зарегестрировались. "
                    f"Теперь вы можете пользоваться услугами нашего магазина!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False
        )
    except SMTPException as error:
        print(error)
