import requests
from tempfile import mkdtemp
from shutil import copy, rmtree
import os
import yaml
import zipfile

from django.conf import settings
from docker.client import DockerClient
from docker.models.images import ImageCollection

from .registry_checker import check_registry


DOCKER_COMPOSE_FILE_DEFAULT_NAME = settings.DOCKER_COMPOSE_FILE_DEFAULT_NAME
DOCKER_REGISTRY_URL = settings.DOCKER_REGISTRY_URL
CALLBACK_URL = f"http://{settings.DEPLOYER_HOSTPORT}/tasks/update/"

check_registry()
docker_client = DockerClient()
ic = ImageCollection(docker_client)


class StackProcessingError(Exception):
    pass


class StackPostProcessingError(Exception):
    pass


def get_dc_file_path(unpacked_stack_path, docker_compose_file_path):
    return os.path.join(unpacked_stack_path, docker_compose_file_path)


def unpack_stack(stack_path):
    temp_dir_name = mkdtemp(prefix='build_')
    full_name = os.path.join(temp_dir_name, os.path.basename(stack_path))
    copy(stack_path, full_name)
    zip_ref = zipfile.ZipFile(stack_path, 'r')
    zip_ref.extractall(temp_dir_name)
    zip_ref.close()
    return temp_dir_name


def get_images_for_building(docker_compose_filename):
    image_build_paths = {}
    with open(docker_compose_filename) as dc_file:
        try:
            config = yaml.safe_load(dc_file)
            services = config['services']
            for name, service in services.items():
                if 'build' in service:
                    image_name = service['image']
                    image_build_paths[image_name] = service['build']
        except yaml.YAMLError as e:
            raise StackProcessingError(f"Can not parse docker-compose config: '{e}'")
        except KeyError as e:
            raise StackProcessingError(f"Invalid docker-compose config. Can not find field: '{e}'")
    return image_build_paths


def build_images(images_for_building, stack_name):
    for image_name, build_path in images_for_building.items():
        full_tag = f'{DOCKER_REGISTRY_URL}/{stack_name}_{image_name}:latest'
        if not os.path.isdir(build_path):
            raise StackProcessingError(f"For image '{image_name}' build path '{build_path}' is not a directory")
        ic.build(path=build_path, tag=full_tag, rm=True)


def push_images(images_for_building, stack_name):
    for image_name, build_path in images_for_building.items():
        full_tag = f'{DOCKER_REGISTRY_URL}/{stack_name}_{image_name}:latest'
        ic.push(full_tag)


def clear_images(images_for_building, stack_name):
    for image_name, build_path in images_for_building.items():
        full_tag = f'{DOCKER_REGISTRY_URL}/{stack_name}_{image_name}:latest'
        ic.remove(image=full_tag)


def process_stack(stack_path, stack_name):
    temp_dir = unpack_stack(stack_path)
    os.chdir(temp_dir)

    dc_file_path = get_dc_file_path(temp_dir, DOCKER_COMPOSE_FILE_DEFAULT_NAME)
    if not os.path.exists(dc_file_path):
        raise StackProcessingError(f"Can not find docker-compose file: '{dc_file_path}'")

    images_for_building = get_images_for_building(dc_file_path)
    build_images(images_for_building, stack_name)
    push_images(images_for_building, stack_name)

    try:
        clear_images(images_for_building, stack_name)
        rmtree(temp_dir)
    except Exception as e:
        raise StackPostProcessingError(e)


def send_update(stack_name):
    full_callback_url = CALLBACK_URL + stack_name
    r = requests.post(full_callback_url)
    if not r.ok:
        raise StackPostProcessingError(f"Callback response is not ok: {r}, {r.content}")
