from .services import MailService

mail_service = MailService()


def check_mailing_list():
    """
    Using MailService to process active mailings.
    """
    mail_service.process_mailing_list()
