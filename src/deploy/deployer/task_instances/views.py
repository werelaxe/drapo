from django.core.files import File
from django.forms import model_to_dict
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from . import models
from .utils import get_adjusted_dc_config
from .celery_tasks import deploy_task_instance
import tasks.models


class TaskInstanceListView(APIView):
    def get(self, request, id):
        if id is None:
            query_set = models.TaskInstance.objects.all()
        else:
            query_set = models.TaskInstance.objects.filter(id=id)
        result = []
        for task in query_set:
            prepared_task = model_to_dict(task)
            result.append(prepared_task)
        return Response(result)


class TaskInstanceAddView(APIView):
    def post(self, request: Request, format=None):
        if 'task_name' not in request.GET:
            return Response("task_name is required as URL parameter", status=HTTP_400_BAD_REQUEST)
        task_name = request.GET['task_name']
        try:
            task = tasks.models.Task.objects.get(pk=task_name)
        except tasks.models.Task.DoesNotExist:
            return Response(f"Task with name={task_name} does not exist", status=HTTP_400_BAD_REQUEST)
        adjusted_dc_config_path = get_adjusted_dc_config(task)
        new_task_instance = models.TaskInstance.objects.create(
            task=task,
        )
        new_task_instance.dc_config = File(open(adjusted_dc_config_path), 'dc_config.yml')
        new_task_instance.save()
        return Response(status=HTTP_204_NO_CONTENT)


class TaskInstanceDeployView(APIView):
    def post(self, request: Request, id, format=None):
        task_instance = get_object_or_404(models.TaskInstance.objects.filter(id=id))
        deploy_task_instance.delay(task_instance.id)
        return Response(status=HTTP_204_NO_CONTENT)
