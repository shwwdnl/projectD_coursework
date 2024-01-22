from django.contrib import admin

from .models import Client, Periods, Mailing, Audience, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')


@admin.register(Periods)
class PeriodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = (
        'time',
        'mailing',
        'client',
        'status',
    )
