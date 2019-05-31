import os

from django.conf import settings
from django.db import models


def context_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, str(instance.id))


class FileContext(models.Model):
    name = models.TextField(max_length=100)
    context = models.FileField(upload_to=context_file_path)
    download_url = models.TextField()

    def delete(self, using=None, keep_parents=False):
        os.remove(self.context.name)
        super(FileContext, self).delete(using=using, keep_parents=keep_parents)


class Task(models.Model):
    ADDED_STATUS = 'added'
    ERROR_STATUS = 'error'
    ENQUEUED_STATUS = 'enqueued'
    READY_TO_DEPLOY = 'ready'
    PROCESSING_STATUS = 'processing'
    DEPLOYED = 'deployed'

    POSSIBLE_STATUSES = (
        (ERROR_STATUS, "Error was occurred while processing"),
        (ENQUEUED_STATUS, "Enqueued"),
        (READY_TO_DEPLOY, "Stack successfully built and pushed. Task is ready to deploy"),
        (PROCESSING_STATUS, "Processing"),
        (DEPLOYED, "Deployed"),
        (ADDED_STATUS, "Task added")
    )
    name = models.CharField(max_length=100, primary_key=True)
    filecontext = models.ForeignKey(FileContext, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=POSSIBLE_STATUSES,
    )
    error_text = models.TextField()
