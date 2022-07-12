
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management import call_command

# Add template extensions
from django.template.loader import render_to_string

HTML = '.html'
TEXT = '.txt'


def format_email(template=None, data=None, message=None):
    if template:
        txt = render_to_string(template.format(TEXT), {'data': data, })
        html = render_to_string(template.format(HTML), {'data': data, })
        return txt, html
    elif message:
        return message, ''
    else:
        return '', ''


@shared_task
def process_notifications():
    call_command('process_notifications')


@shared_task
def send_email(subject, to, template=None, data=None, message=None):
    message, html_message = format_email(template, data, message)

    message = EmailMultiAlternatives(subject, message, settings.EMAIL_FROM_ADDRESS, [to])
    if template:
        message.attach_alternative(html_message, "text/html")
    message.send()
