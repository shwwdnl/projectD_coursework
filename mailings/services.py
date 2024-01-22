import logging
from smtplib import SMTPException

from django.core.mail import send_mail
from django.utils import timezone

from config.settings import DEFAULT_FROM_EMAIL
from .models import Mailing, Client, MailingLog

logging.basicConfig(level=logging.INFO, filename="log.log")


class MailingStatusesService:

    @staticmethod
    def set_finished(mailing: Mailing):
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save()

    @staticmethod
    def set_started(mailing: Mailing):
        mailing.status = Mailing.STATUS_STARTED
        mailing.save()

    @staticmethod
    def get_mailings_list():
        return Mailing.objects.all()

    def update_statuses(self):
        mailings_list = self.get_mailings_list()

        now = timezone.now()

        for mailing in mailings_list:

            if mailing.start_time <= now < mailing.end_time:
                self.set_started(mailing)
            elif mailing.end_time <= now:
                self.set_finished(mailing)


class MailService(MailingStatusesService):
    """
    Service class for email sending.
    Checking active mailings and run email sending.
    Used in crontab schedule
    """

    @staticmethod
    def get_started_mailings():
        return Mailing.objects.filter(status=Mailing.STATUS_STARTED)

    @staticmethod
    def send_one_email(mailing: Mailing, recipient: Client):
        try:
            result = send_mail(
                subject=mailing.message_title,
                from_email=DEFAULT_FROM_EMAIL,
                message=mailing.message_body,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
        except SMTPException as ex:
            error_message = ex
            status = MailingLog.STATUS_ERROR
        else:
            error_message = None
            status = MailingLog.STATUS_SUCCESS if result else MailingLog.STATUS_FAILED
        finally:
            log_obj = MailingLog(
                client=recipient,
                mailing=mailing,
                status=status,
                error_message=error_message,
            )
            log_obj.save()

    def process_mailing(self, mailing: Mailing):

        recipients = mailing.audience.recipients.all()
        logging.info(f"recipients: {recipients}")

        for recipient in recipients:
            last_log: MailingLog = recipient.logs.filter(mailing=mailing).last()
            if not last_log or (timezone.now() - last_log.time >= mailing.period.duration):
                self.send_one_email(mailing, recipient)

    def process_mailing_list(self):

        self.update_statuses()

        mailings = self.get_started_mailings()

        logging.info(f"mailings: {mailings}")

        for mailing in mailings:
            self.process_mailing(mailing)
