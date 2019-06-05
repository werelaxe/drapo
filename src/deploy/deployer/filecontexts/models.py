import os
from django.conf import settings
from django.db import models


def context_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, str(instance.id))


def dc_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, settings.COMPOSE_CONFIGS_STORAGE_SUBDIR, f"{instance.id}.yml")


class FileContext(models.Model):
    ENQUEUED_STATUS = 'enqueued'
    PROCESSING_STATUS = 'processing'
    ERROR_STATUS = 'error'
    CORRECT_STATUS = 'correct'

    POSSIBLE_STATUSES = (
        (ENQUEUED_STATUS, "Enqueued"),
        (ERROR_STATUS, "Error was occurred while checking context correctness"),
        (PROCESSING_STATUS, "Processing"),
        (CORRECT_STATUS, "File context passed the correctness checking"),
    )
    status = models.CharField(
        max_length=10,
        choices=POSSIBLE_STATUSES,
    )

    name = models.TextField(max_length=100)
    context = models.FileField(upload_to=context_file_path)
    dc_file = models.FileField(upload_to=dc_file_path, blank=True, default=None, null=True)
    download_url = models.TextField()
    error_text = models.TextField()

    def delete(self, using=None, keep_parents=False):
        os.remove(self.context.name)
        super(FileContext, self).delete(using=using, keep_parents=keep_parents)
