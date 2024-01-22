from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        managers_group = Group.objects.filter(name="Managers").first()
        content_group = Group.objects.filter(name="Content managers").first()

        if not (managers_group and content_group):
            self.stdout.write(
                self.style.ERROR(
                    "To run the command, the 'Managers' and 'Content managers' groups must be created beforehand.\n"
                    "Execute the command 'python3 manage.py load_groups' for automatic group creation."
                )
            )
            return

        manager_email = "manager@sample.ru"
        manager_psw = get_random_string(length=8)

        content_email = "content@sample.ru"
        content_psw = get_random_string(length=8)

        try:
            manager = User.objects.create(
                email=manager_email,
                first_name="Manager",
                last_name="Sample",
                is_staff=False,
            )

            manager.set_password(manager_psw)
            manager.groups.add(managers_group)
            manager.save()

            content = User.objects.create(
                email=content_email,
                first_name="Content Manager",
                last_name="Sample",
                is_staff=True,
            )

            content.set_password(content_psw)
            content.groups.add(content_group)
            content.save()

        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"Error: {ex}"))

        else:
            success_message = (f"Successful created staff:\n"
                               f"Manager: {manager_email}, password: {manager_psw}.\n"
                               f"Content manager: {content_email}, password: {content_psw}.")
            self.stdout.write(self.style.SUCCESS(success_message))
