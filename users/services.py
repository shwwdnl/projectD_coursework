from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from users import texts


def send_verify_mail(user, request):

    current_site = get_current_site(request)
    mail_subject = texts.register_mail_subject.format(current_site)
    token = default_token_generator.make_token(user)
    to_email = user.email

    message = render_to_string(
        "users/email_templates/confirm_email_message.html",
        {
            "user": user,
            "current_site": current_site,
            "domain": current_site.domain,
            "uid": user.uid,
            "token": token,
        },
    )

    activation_email = EmailMessage(subject=mail_subject, body=message, to=[to_email])

    activation_email.content_subtype = "html"
    activation_email.send()


def manager_or_superuser(user):
    return user.groups.filter(name='Managers').exists() or user.is_superuser
