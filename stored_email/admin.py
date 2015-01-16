from django.contrib import admin
from stored_email.models import EMail, EMailAlternative


class EMailAlternativeInline(admin.TabularInline):
    model = EMailAlternative
    extra = 1


class EMailAdmin(admin.ModelAdmin):
    readonly_fields = ('sent', 'queued')
    list_display = ('subject', 'from_email', 'to_emails', 'sent')
    inlines = [EMailAlternativeInline,]


admin.site.register(EMail, EMailAdmin)
