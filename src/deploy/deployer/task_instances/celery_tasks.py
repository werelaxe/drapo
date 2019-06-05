from .deploy.docker_wrapper import docker_stack_deploy
from .celery import app
from .models import TaskInstance


@app.task
def deploy_task_instance(task_instance_id):
    task_instance = TaskInstance.objects.get(pk=task_instance_id)
    docker_stack_deploy(task_instance.dc_config.file.name, f"{task_instance.task.name}_{task_instance.id}")
