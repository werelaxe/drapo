from django.contrib import admin

from . import models


class StackAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'error_text', 'context', 'download_url')


admin.site.register(models.Stack, StackAdmin)
