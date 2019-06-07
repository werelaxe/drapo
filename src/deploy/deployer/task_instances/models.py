import os

from django.db import models
from django.db.models import DO_NOTHING
from django.conf import settings
from tasks.models import Task


def ti_dc_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, settings.DC_TI_CONFIGS_STORAGE_SUBDIR, f"{instance.id}.yml")


class TaskInstance(models.Model):
    ADDED_STATUS = 'added'
    ENQUEUED_STATUS = 'enqueued'
    DEPLOYING_STATUS = 'deploying'
    DEPLOYED_STATUS = 'deployed'
    ERROR_STATUS = 'error'
    UNDEPLOYING_STATUS = 'undeploying'

    POSSIBLE_STATUSES = (
        (ADDED_STATUS, "Added to database"),
        (ENQUEUED_STATUS, "Enqueued for processing"),
        (DEPLOYING_STATUS, "Deploying in progress"),
        (DEPLOYED_STATUS, "Deployed"),
        (ERROR_STATUS, "Error was occurred"),
        (UNDEPLOYING_STATUS, "Undeploying in progress"),
    )
    status = models.CharField(
        max_length=10,
        choices=POSSIBLE_STATUSES,
    )

    task = models.ForeignKey(Task, on_delete=DO_NOTHING)
    dc_config = models.FileField(upload_to=ti_dc_file_path)
    error_text = models.TextField()
