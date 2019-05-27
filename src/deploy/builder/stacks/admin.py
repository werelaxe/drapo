from django.contrib import admin

from . import models


class StackAdmin(admin.ModelAdmin):
    list_display = ('name', 'context', 'download_url')


admin.site.register(models.Stack, StackAdmin)
