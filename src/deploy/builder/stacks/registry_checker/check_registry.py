import json
import os
import requests

from django.conf import settings


DOCKER_DAEMON_CONF_PATH = settings.DOCKER_DAEMON_CONF_PATH
DOCKER_REGISTRY_URL = settings.DOCKER_REGISTRY_URL


class InappropriateDockerDaemonConfigError(Exception):
    pass


class RegistryInaccessibleError(Exception):
    pass


def check_registry_config(docker_daemon_conf_path=DOCKER_DAEMON_CONF_PATH):
    if not os.path.exists(docker_daemon_conf_path):
        raise InappropriateDockerDaemonConfigError(f"config file '{docker_daemon_conf_path}' does not exist")

    with open(docker_daemon_conf_path) as docker_conf_file:
        docker_conf = json.load(docker_conf_file)
        if 'insecure-registries' not in docker_conf:
            raise InappropriateDockerDaemonConfigError(
                "config does not contain 'insecure-registries' field. "
                f'Add "insecure-registries":["{DOCKER_REGISTRY_URL}"]'
            )
        if DOCKER_REGISTRY_URL not in docker_conf['insecure-registries']:
            raise InappropriateDockerDaemonConfigError(
                f'config does not contain insecure registry {DOCKER_REGISTRY_URL}'
            )


def check_registry_accessibility(docker_registry_url=DOCKER_REGISTRY_URL):
    try:
        r = requests.get("http://" + docker_registry_url, timeout=5)
        if not r.ok:
            raise RegistryInaccessibleError("Registry response is not ok: " + r.status_code)
    except requests.exceptions.ConnectionError as e:
        raise RegistryInaccessibleError(e)


def check_registry():
    check_registry_config()
    check_registry_accessibility()
