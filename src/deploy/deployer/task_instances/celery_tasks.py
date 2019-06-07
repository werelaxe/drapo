from .deploy.docker_wrapper import docker_stack_deploy, docker_stack_rm
from .celery import app
from .models import TaskInstance


@app.task
def deploy_task_instance(task_instance_id):
    task_instance = TaskInstance.objects.get(pk=task_instance_id)
    try:
        task_instance.status = TaskInstance.DEPLOYING_STATUS
        task_instance.save()
        docker_stack_deploy(task_instance.dc_config.file.name, f"{task_instance.task.name}_{task_instance.id}")
        task_instance.status = TaskInstance.DEPLOYED_STATUS
        task_instance.save()
    except Exception as e:
        task_instance.status = TaskInstance.ERROR_STATUS
        task_instance.error_text = f"Error while deploying: {e}"
        task_instance.save()


@app.task
def undeploy_task_instance(task_instance_id):
    task_instance = TaskInstance.objects.get(pk=task_instance_id)
    try:
        task_instance.status = TaskInstance.UNDEPLOYING_STATUS
        task_instance.save()
        docker_stack_rm(f"{task_instance.task.name}_{task_instance.id}")
        task_instance.status = TaskInstance.ADDED_STATUS
        task_instance.save()
    except Exception as e:
        task_instance.status = TaskInstance.ERROR_STATUS
        task_instance.error_text = f"Error while undeploying: {e}"
        task_instance.save()
