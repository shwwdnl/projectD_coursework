# Generated by Django 4.2.6 on 2023-11-22 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailings", "0013_alter_mailing_options_mailing_creator"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "permissions": [
                    ("stop_mailing", "Can stop mailing"),
                    ("view_all_mailings", "Can view all mailings"),
                ],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
    ]
