import yaml
from random import randint
from tempfile import mkstemp

from django.conf import settings
from tasks.config import parse_task_config


def get_free_port():
    return randint(1024, 65536)


def get_adjusted_dc_config(task):
    dc_config = yaml.safe_load(task.filecontext.dc_file)
    task_config = parse_task_config(task.config_text)

    for service_name, service in dc_config['services'].items():
        if 'build' in service:
            service['image'] = f"{settings.DOCKER_REGISTRY_URL}/{task.name}_" + service['image']
        if service_name in task_config.services:
            service_config = task_config.services[service_name]
            service_ports = []
            for open_port in service_config['ports']:
                service_ports.append(f'{get_free_port()}:{open_port}')
            service['ports'] = service_ports

    return create_temp_dc_file(dc_config)


def create_temp_dc_file(dc_config):
    _, temp_filename = mkstemp(prefix='dc_config_')
    with open(temp_filename, "w") as temp_dc_file:
        yaml.safe_dump(dc_config, temp_dc_file)
    return temp_filename
