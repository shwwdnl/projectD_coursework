from smtplib import SMTPDataError

from django.core.mail import send_mail

from blog.models import Article
from django.conf import settings


def send_congratulatory_mail(article: Article):
    subject = "SkyStore - статья пользуется популярностью!"
    body = f'Ваша статья "{article.title}" набрала {article.views_count} просмотров!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [article.author.email]

    try:
        send_mail(subject, body, from_email=from_email, recipient_list=recipient_list)
    except SMTPDataError as ex:
        print(f"Ошибка отправки письма:\n{ex}")
