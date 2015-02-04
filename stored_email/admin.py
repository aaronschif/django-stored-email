from django.contrib import admin
from stored_email.models import EMail, EMailAlternative, EMailAttachment


def formatted_emails(obj):
    displayed_emails = obj.to[:3]
    if len(obj.to) > 3:
        displayed_emails.append('... [{} others]'.format(len(obj.to)-3))
    return ', '.join(displayed_emails)
formatted_emails.short_description = "To Emails"


class EMailAlternativeInline(admin.TabularInline):
    model = EMailAlternative
    extra = 1


class EMailAttachmentInline(admin.TabularInline):
    model = EMailAttachment
    extra = 0


class EMailAdmin(admin.ModelAdmin):
    readonly_fields = ('sent', 'queued')
    list_display = ('subject', 'from_email', formatted_emails, 'sent')
    list_filter = ('sent',)
    inlines = [EMailAlternativeInline, EMailAttachmentInline]


admin.site.register(EMail, EMailAdmin)
