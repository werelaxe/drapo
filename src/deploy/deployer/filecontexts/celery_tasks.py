import os

from django.core.files import File

from .celery import app
from .models import FileContext
from .common import unpack_filecontext, get_dc_file_path, DOCKER_COMPOSE_FILENAME


@app.task
def process_filecontext(filcontext_id):
    filecontext = FileContext.objects.get(id=filcontext_id)
    if filecontext.status == FileContext.CORRECT_STATUS:
        return
    filecontext.status = FileContext.PROCESSING_STATUS
    filecontext.save()

    temp_dir = unpack_filecontext(filecontext.context.file)
    dc_file_path = get_dc_file_path(temp_dir)
    if not os.path.exists(dc_file_path):
        filecontext.status = FileContext.ERROR_STATUS
        filecontext.error_text = f"Can not find {DOCKER_COMPOSE_FILENAME} in files"
        filecontext.save()
        return

    filecontext.dc_file = File(open(dc_file_path), filecontext.name)
    filecontext.status = FileContext.CORRECT_STATUS
    filecontext.save()
