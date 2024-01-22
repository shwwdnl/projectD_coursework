from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from blog.models import Article
from mailings.models import Mailing, Client, Audience, MailingLog
from users.models import User


class Command(BaseCommand):
    help = "Create groups and assign permissions"

    def handle(self, *args, **options):

        managers_group, managers_created = Group.objects.get_or_create(name="Managers")
        content_managers_group, content_managers_created = Group.objects.get_or_create(
            name="Content managers"
        )
        service_users_group, service_users_created = Group.objects.get_or_create(
            name="Service users"
        )

        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        mailing_log_content_type = ContentType.objects.get_for_model(MailingLog)
        users_content_type = ContentType.objects.get_for_model(User)
        article_content_type = ContentType.objects.get_for_model(Article)
        client_content_type = ContentType.objects.get_for_model(Client)
        audience_content_type = ContentType.objects.get_for_model(Audience)

        view_mailings, _ = Permission.objects.get_or_create(
            codename="view_mailing", content_type=mailing_content_type
        )
        change_mailing, _ = Permission.objects.get_or_create(
            codename="change_mailing", content_type=mailing_content_type
        )
        add_mailing, _ = Permission.objects.get_or_create(
            codename="add_mailing", content_type=mailing_content_type
        )
        delete_mailing, _ = Permission.objects.get_or_create(
            codename="delete_mailing", content_type=mailing_content_type
        )
        stop_mailing, _ = Permission.objects.get_or_create(
            codename="stop_mailing",
            name="Can stop mailing",
            content_type=mailing_content_type,
        )
        start_mailing, _ = Permission.objects.get_or_create(
            codename="start_mailing",
            name="Can start mailing",
            content_type=mailing_content_type,
        )

        view_users, _ = Permission.objects.get_or_create(
            codename="view_user", content_type=users_content_type
        )
        block_users, _ = Permission.objects.get_or_create(
            codename="block_user",
            name="Can block user",
            content_type=users_content_type,
        )
        activate_user, _ = Permission.objects.get_or_create(
            codename="activate_user",
            name="Can activate user",
            content_type=users_content_type,
        )
        add_article, _ = Permission.objects.get_or_create(
            codename="add_article", content_type=article_content_type
        )
        change_article, _ = Permission.objects.get_or_create(
            codename="change_article", content_type=article_content_type
        )
        delete_article, _ = Permission.objects.get_or_create(
            codename="delete_article", content_type=article_content_type
        )

        add_client, _ = Permission.objects.get_or_create(
            codename="add_client", content_type=client_content_type
        )
        view_client, _ = Permission.objects.get_or_create(
            codename="view_client", content_type=client_content_type
        )
        change_client, _ = Permission.objects.get_or_create(
            codename="change_client", content_type=client_content_type
        )
        delete_client, _ = Permission.objects.get_or_create(
            codename="delete_client", content_type=client_content_type
        )

        add_audience, _ = Permission.objects.get_or_create(
            codename="add_audience", content_type=audience_content_type
        )
        view_audience, _ = Permission.objects.get_or_create(
            codename="view_audience", content_type=audience_content_type
        )
        change_audience, _ = Permission.objects.get_or_create(
            codename="change_audience", content_type=audience_content_type
        )
        delete_audience, _ = Permission.objects.get_or_create(
            codename="delete_audience", content_type=audience_content_type
        )

        view_mailing_log, _ = Permission.objects.get_or_create(
            codename="view_mailinglog", content_type=mailing_log_content_type
        )

        managers_group.permissions.add(
            view_mailings,
            view_users,
            block_users,
            activate_user,
            stop_mailing,
            start_mailing,
            view_mailing_log,
        )

        content_managers_group.permissions.add(
            add_article,
            change_article,
            delete_article,
        )

        service_users_group.permissions.add(
            add_mailing,
            change_mailing,
            delete_mailing,
            view_mailings,
            stop_mailing,
            start_mailing,
            add_client,
            view_client,
            change_client,
            delete_client,
            add_audience,
            view_audience,
            change_audience,
            delete_audience,
            view_mailing_log,
        )

        if managers_created:
            message = (
                "Managers group were successfully created. Permissions was be added."
            )
        else:
            message = "Managers group already exists. Permissions was be updated."
        self.stdout.write(self.style.SUCCESS(message))

        if content_managers_created:
            message = "Content managers group were successfully created. Permissions was be added."
        else:
            message = (
                "Content managers group already exists. Permissions was be updated."
            )
        self.stdout.write(self.style.SUCCESS(message))

        if service_users_created:
            message = "Service users group were successfully created. Permissions was be added."
        else:
            message = "Service users group already exists. Permissions was be updated."
        self.stdout.write(self.style.SUCCESS(message))
