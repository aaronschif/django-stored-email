from django.conf import settings
from django.core.mail import get_connection

from celery import shared_task

from stored_email.models import EMail


@shared_task()
def send_email_batch(batch_size=None):

    conn = get_connection(
        backend=getattr(settings, 'STORED_EMAIL_BACKEND',
                        'django.core.mail.backends.smtp.EmailBackend'))
    try:
        conn.open()
        if batch_size:
            emails = EMail.objects.filter(sent=False)[:batch_size]
        else:
            emails = EMail.objects.filter(sent=False)

        for email in emails:
            email.send(connection=conn)

    finally:
        conn.close()


@shared_task()
def send_emails(ids):
    conn = get_connection(
        backend=getattr(settings, 'STORED_EMAIL_BACKEND',
                        'django.core.mail.backends.smtp.EmailBackend'))
    emails = [email for email in EMail.objects.filter(id__in=ids)]

    try:
        conn.open()
        for email in emails:
            email.send(connection=conn)

    finally:
        conn.close()
