from django.conf import settings
from random import randint

from apps.common.tasks import send_email


def generate_token(token_length):
    range_start = 10 ** (token_length - 1)
    range_end = (10 ** token_length) - 1
    return randint(range_start, range_end)


def send_mail(subject, to, template=None, data=None, message=None):
    if settings.ENABLE_CELERY:
        send_email.delay(subject, to, template, data, message)
    else:
        send_email(subject, to, template, data, message)
