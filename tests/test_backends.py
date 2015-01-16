import pytest
from django.core.mail import get_connection
from django.core import mail

from stored_email.backends import CeleryEmailBackend
from stored_email.models import EMail, EMailAttachment
