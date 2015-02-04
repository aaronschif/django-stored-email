from email.mime.base import MIMEBase

from django.db import models
from django.core.mail import EmailMultiAlternatives, get_connection, \
    EmailMessage
from django.conf import settings
from django.core.files.base import ContentFile

from fields import EmailsListField, EmailHeadersField


class EMail(models.Model):
    class Meta:
        verbose_name = 'Email'

    def __init__(self, *args, **kwargs):
        queue = kwargs.pop('queue', None)
        super(EMail, self).__init__(*args, **kwargs)

        if queue:
            self.queue = queue

    @classmethod
    def create_from_message(cls, message, queue=None):
        assert isinstance(message, EmailMessage)
        message_model = cls(queue=queue)
        message_model.subject = message.subject
        message_model.body = message.body

        message_model.to = message.to
        message_model.cc = message.cc
        message_model.bcc = message.bcc

        message_model.from_email = message.from_email

        message_model.extra_headers = message.extra_headers

        message_model.save()
        if hasattr(message, 'alternatives'):
            for c in message.alternatives:
                alt = EMailAlternative()
                alt.message = message_model
                alt.content = c[0]
                alt.mimetype = c[1]
                alt.save()

        if hasattr(message, 'attachments'):
            for c in message.attachments:
                if isinstance(c, (tuple, list)) and len(c) is 3:
                    filename, content, mimetype = c
                    att = EMailAttachment()
                    att.message = message_model
                    att.filename = filename
                    att.content = ContentFile(content, filename)
                    att.mimetype = mimetype
                    att.save()
                elif isinstance(c, MIMEBase):
                    raise NotImplementedError()

        return message_model

    def __unicode__(self):
        to_emails = self.to[:3]
        if self.to[3:]:
            to_emails.append('...')
        return "<'{m.subject}' From: {m.from_email} To: {to_emails}>"\
            .format(m=self, to_emails=', '.join(to_emails))

    def message(self):
        m = EmailMultiAlternatives(self.subject, self.body)
        m.to = self.to
        m.cc = self.cc
        m.bcc = self.bcc
        m.from_email = self.from_email

        m.alternatives = \
            [(att.content, att.mimetype) for att in self.alternatives()]
        for attachment in self.attachments():
            m.attach(attachment.filename, attachment.content.read(),
                     attachment.mimetype)

        m.extra_headers = self.extra_headers

        return m

    def send(self, connection=None):
        if not connection:
            connection = get_connection(
                backend=getattr(settings, 'STORED_EMAIL_BACKEND',
                                'django.core.mail.backends.smtp.EmailBackend'))
        connection.send_messages([self.message()])
        self.sent = True
        self.save()

    def attachments(self):
        return EMailAttachment.objects.filter(message=self)

    def alternatives(self):
        return EMailAlternative.objects.filter(message=self)

    subject = models.CharField(max_length=250)
    body = models.TextField()

    to = EmailsListField()
    cc = EmailsListField(blank=True)
    bcc = EmailsListField(blank=True)

    from_email = models.EmailField()

    extra_headers = EmailHeadersField(blank=True)

    # connection = None

    sent = models.BooleanField(default=False)
    queued = models.DateField(auto_now=True)
    queue = models.CharField(max_length=200, default='default')


class EMailAlternative(models.Model):
    message = models.ForeignKey(EMail)

    content = models.TextField()
    mimetype = models.CharField(max_length=200, default='text/html')


class EMailAttachment(models.Model):
    message = models.ForeignKey(EMail)

    filename = models.CharField(max_length=200)
    content = models.FileField(upload_to='stored_email')
    mimetype = models.CharField(max_length=200, blank=True, null=True)
