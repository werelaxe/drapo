from django.contrib import admin


from . import models


class FileContextAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'context', 'download_url')


admin.site.register(models.FileContext, FileContextAdmin)
