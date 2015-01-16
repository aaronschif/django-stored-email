import re
import six

from django.core.validators import validate_email
from django.db.models import TextField, SubfieldBase
from django.utils.translation import ugettext as _
from django import forms


class EmailsFormField(forms.Field):
    def prepare_value(self, value):
        if value is None:
            return ''
        elif isinstance(value, six.string_types):
            return value
        else:
            return ',\n'.join(value)


class EmailsListField(TextField):
    __metaclass__ = SubfieldBase
    email_separator_re = re.compile(r'\s*,\s*')

    def to_python(self, value):
        if isinstance(value, six.string_types):
            return [x for x in self.email_separator_re.split(value) if x]
        else:
            return list(value)

    def validate(self, value, model_instance):
        super(EmailsListField, self).validate(value, model_instance)

        for email in value:
            validate_email(email)

    def get_prep_value(self, value):
        if isinstance(value, six.string_types):
            return value
        else:
            return ', '.join(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': EmailsFormField}
        defaults.update(kwargs)
        return super(EmailsListField, self).formfield(**defaults)


class EmailHeadersFormField(forms.Field):
    def prepare_value(self, value):
        if value is None:
            return ''
        elif isinstance(value, six.string_types):
            return value
        else:
            result = []
            for key, value in value.items():
                result.append(key)
                result.append(':')
                result.append(value)
                result.append('\n')
            return ''.join(result)


class EmailHeadersField(TextField):
    __metaclass__ = SubfieldBase

    def to_python(self, value):
        if isinstance(value, six.string_types):
            result = {}
            for line in value.split('\n'):
                if not line:
                    continue
                key, value = line.split(':', 1)
                result[key] = value
            return result
        else:
            return value

    def get_prep_value(self, value):
        if isinstance(value, six.string_types):
            return value
        else:
            result = []
            for key, value in value.items():
                result.append(key)
                result.append(':')
                result.append(value)
                result.append('\n')
            return ''.join(result)

    def formfield(self, **kwargs):
        defaults = {'form_class': EmailHeadersFormField}
        defaults.update(kwargs)
        return super(EmailHeadersField,self).formfield(**defaults)
