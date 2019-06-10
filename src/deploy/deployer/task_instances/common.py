import yaml
from docker.models.services import ServiceCollection
from docker.models.nodes import NodeCollection
from docker.client import DockerClient


client = DockerClient()
sc = ServiceCollection(client)
nc = NodeCollection(client)


class InfoGettingError(Exception):
    pass


def get_task_instance_config(task_instance):
    config_file = task_instance.dc_config.file
    return yaml.safe_load(config_file)


def get_services2ports(task_instance):
    services2ports = {}
    config = get_task_instance_config(task_instance)
    for service_name, service in config['services'].items():
        if 'ports' in service:
            services2ports[service_name] = [int(e.split(':')[0]) for e in service['ports']]
    return services2ports


def get_services_name_prefix(task_instance):
    return f"{task_instance.task.name}_{task_instance.id}_"


def get_urls(task_instance):
    urls = []
    service2ports = get_services2ports(task_instance)
    services_name_prefix = get_services_name_prefix(task_instance)
    for service in sc.list():
        if service.name.startswith(services_name_prefix) and service.name[len(services_name_prefix):] in service2ports:
            tasks = service.tasks(filters={'service': service.name, 'desired-state': 'running'})
            if not tasks:
                raise InfoGettingError(f"There is no running services with name: {service.name}")
            task = tasks[0]
            if 'NodeID' not in task:
                raise InfoGettingError(f"Docker task does not contain node related node: {task}")
            task_node_id = task['NodeID']
            node = nc.get(task_node_id)
            ip = node.attrs['Status']['Addr']
            ports = service2ports[service.name[len(services_name_prefix):]]
            addresses = [f"{ip}:{port}" for port in ports]
            urls.extend(addresses)
    return urls
