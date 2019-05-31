from django.contrib import admin

from . import models


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'error_text', 'get_filecontext')

    def get_filecontext(self, obj):
        return f"FileContext(id={obj.filecontext.id}, name={obj.filecontext.name})"


class FileContextAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'context', 'download_url')


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.FileContext, FileContextAdmin)
