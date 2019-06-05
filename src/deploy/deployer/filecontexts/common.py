import os
import zipfile
from tempfile import mkdtemp

from django.conf import settings

DOCKER_COMPOSE_FILENAME = settings.DOCKER_COMPOSE_FILENAME


def unpack_filecontext(context_file):
    temp_dir_name = mkdtemp(prefix='filecontext_')
    zip_ref = zipfile.ZipFile(context_file, 'r')
    zip_ref.extractall(temp_dir_name)
    zip_ref.close()
    return temp_dir_name


def get_dc_file_path(unpacked_stack_path, docker_compose_file_path=DOCKER_COMPOSE_FILENAME):
    return os.path.join(unpacked_stack_path, docker_compose_file_path)
