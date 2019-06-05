import os

from django.db import models
from django.db.models import DO_NOTHING
from django.conf import settings
from tasks.models import Task


def ti_dc_file_path(instance, filename):
    return os.path.join(settings.STORAGE_DIR, settings.DC_TI_CONFIGS_STORAGE_SUBDIR, f"{instance.id}.yml")


class TaskInstance(models.Model):
    task = models.ForeignKey(Task, on_delete=DO_NOTHING)
    dc_config = models.FileField(upload_to=ti_dc_file_path)
