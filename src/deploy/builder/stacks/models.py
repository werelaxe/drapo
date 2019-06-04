import os

from django.db import models
from django.conf import settings


def context_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, filename)


class Stack(models.Model):
    ERROR_STATUS = 'error'
    ENQUEUED_STATUS = 'enqueued'
    PUSHED_STATUS = 'pushed'
    PROCESSING_STATUS = 'processing'

    POSSIBLE_STATUSES = (
        (ERROR_STATUS, "Error was occurred while processing"),
        (ENQUEUED_STATUS, "Enqueued"),
        (PUSHED_STATUS, "Successfully built and pushed"),
        (PROCESSING_STATUS, "Processing")
    )
    name = models.CharField(max_length=100, primary_key=True)
    context = models.FileField(upload_to=context_file_path)
    download_url = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=POSSIBLE_STATUSES,
    )
    error_text = models.TextField()

    def delete(self, using=None, keep_parents=False):
        os.remove(self.context.name)
        super(Stack, self).delete(using=using, keep_parents=keep_parents)
