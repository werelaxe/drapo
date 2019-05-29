import os
from subprocess import run, PIPE

from django.conf import settings


DOCKER_COMPOSE_PATH = settings.DOCKER_COMPOSE_PATH
DOCKER_PATH = settings.DOCKER_PATH


def docker_compose_build(path):
    os.chdir(path)
    result = run(f"{DOCKER_COMPOSE_PATH} build", shell=True, stdout=PIPE, stderr=PIPE)
    return result


def docker_compose_push(path):
    os.chdir(path)
    result = run(f"{DOCKER_COMPOSE_PATH} push", shell=True, stdout=PIPE, stderr=PIPE)
    return result
