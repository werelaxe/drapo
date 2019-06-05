import os

from django.db import models
from django.conf import settings
import filecontexts.models


def context_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, str(instance.id))


class Task(models.Model):
    ADDED_STATUS = 'added'
    ERROR_STATUS = 'error'
    ENQUEUED_STATUS = 'enqueued'
    READY_TO_DEPLOY = 'ready'
    PROCESSING_STATUS = 'processing'

    POSSIBLE_STATUSES = (
        (ERROR_STATUS, "Error was occurred while processing"),
        (ENQUEUED_STATUS, "Enqueued"),
        (READY_TO_DEPLOY, "Stack successfully built and pushed. Task is ready to deploy"),
        (PROCESSING_STATUS, "Processing"),
        (ADDED_STATUS, "Task added")
    )
    name = models.CharField(max_length=100, primary_key=True)
    filecontext = models.ForeignKey(filecontexts.models.FileContext, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=10,
        choices=POSSIBLE_STATUSES,
    )
    error_text = models.TextField()
    config_text = models.TextField()
