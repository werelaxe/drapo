from tempfile import mkdtemp
from shutil import copy, move
import os
import yaml
import zipfile

from django.conf import settings
from .docker_wrapper.docker_commands import docker_compose_build, docker_compose_push


DOCKER_COMPOSE_FILE_DEFAULT_NAME = settings.DOCKER_COMPOSE_FILE_DEFAULT_NAME
DOCKER_REGISTRY_URL = settings.DOCKER_REGISTRY_URL


class StackProcessingError(Exception):
    pass


def check_result(result):
    if result.returncode:
        raise StackProcessingError(
            f"Error while executing command '{result.args}', "
            f"stdout={result.stdout}, stderr={result.stderr}"
        )


def unpack_stack(stack_path):
    temp_dir_name = mkdtemp(prefix='build_')
    full_name = os.path.join(temp_dir_name, os.path.basename(stack_path))
    copy(stack_path, full_name)
    zip_ref = zipfile.ZipFile(stack_path, 'r')
    zip_ref.extractall(temp_dir_name)
    zip_ref.close()
    return temp_dir_name


def adjust_docker_compose_file(temp_stack_path, stack_name):
    docker_compose_filename = os.path.join(temp_stack_path, DOCKER_COMPOSE_FILE_DEFAULT_NAME)
    if not os.path.exists(docker_compose_filename):
        raise StackProcessingError(f"Can not find file '{DOCKER_COMPOSE_FILE_DEFAULT_NAME}' in stack root")
    new_docker_compose_filename = docker_compose_filename + '_new'
    with open(docker_compose_filename) as dc_file, open(new_docker_compose_filename, 'w') as new_dc_file:
        try:
            config = yaml.safe_load(dc_file)
            services = config['services']
            for service_name, service in services.items():
                if 'build' in service:
                    service['image'] = f"{DOCKER_REGISTRY_URL}/{stack_name}_{service['image']}"
            yaml.safe_dump(config, new_dc_file)
        except yaml.YAMLError as e:
            raise StackProcessingError("Can not parse docker-compose config: " + str(e))
        except KeyError as e:
            raise StackProcessingError(f"Invalid config: {config}. Can not find field {e}")
    os.remove(docker_compose_filename)
    move(new_docker_compose_filename, docker_compose_filename)


def build_stack(stack_path, stack_name):
    temp_dir = unpack_stack(stack_path)
    adjust_docker_compose_file(temp_dir, stack_name)
    result = docker_compose_build(temp_dir)
    check_result(result)
    return temp_dir, result


def push_stack(built_stack_path):
    result = docker_compose_push(built_stack_path)
    check_result(result)


def process_stack(stack_path, stack_name):
    built_stack_path, build_result = build_stack(stack_path, stack_name)
    push_stack(built_stack_path)
