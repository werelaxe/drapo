import json
import requests
import traceback
import yaml
from django.core import serializers
from django.core.files import File
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.conf import settings


from .config import parse_task_config, InvalidTaskConfigError
from .builder_api import BuilderApi, StackStatus
from . import models
import filecontexts.models


builder_api = BuilderApi(settings.BUILDER_HOSTPORT, settings.BUILDER_TOKEN)


class TaskAddView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request: Request, name=None, format=None):
        config_file = request.FILES['file']
        config_text = config_file.file.read()
        try:
            parse_task_config(config_text)
        except InvalidTaskConfigError as e:
            return Response(f"Invalid task config: {config_text}, error: {e}", status=HTTP_400_BAD_REQUEST)

        tasks = list(models.Task.objects.filter(name=name))
        if tasks:
            if tasks[0].status != models.Task.ERROR_STATUS:
                return Response(f"Task '{name}' already exists", status=HTTP_400_BAD_REQUEST)
            else:
                tasks[0].delete()

        if 'filecontext' not in request.GET:
            return Response("Filecontext id is required as URL parameter", status=HTTP_400_BAD_REQUEST)
        filecontext_id = request.GET['filecontext']
        try:
            file_context = filecontexts.models.FileContext.objects.get(pk=filecontext_id)
            if file_context.status != filecontexts.models.FileContext.CORRECT_STATUS:
                return Response(
                    f"File context with id={filecontext_id} has not correct status",
                    status=HTTP_400_BAD_REQUEST
                )
        except filecontexts.models.FileContext.DoesNotExist:
            return Response(f"File context with id={filecontext_id} does not exist", status=HTTP_400_BAD_REQUEST)

        new_task = models.Task.objects.create(
            name=name,
            status=models.Task.ADDED_STATUS,
            filecontext=file_context,
            config_text=config_text.decode(),
        )
        try:
            builder_api.upload_stack(name, file_context.context.file.read())
        except Exception:
            new_task.status = models.Task.ERROR_STATUS
            new_task.error_text = f"Builder api calling error: {traceback.format_exc()}"
            new_task.save()
            raise
        return Response(status=HTTP_204_NO_CONTENT)


class TaskListView(APIView):
    def get(self, request, name):
        if name is None:
            query_set = models.Task.objects.all()
        else:
            query_set = models.Task.objects.filter(name=name)
        result = []
        for task in query_set:
            prepared_task = model_to_dict(task)
            result.append(prepared_task)
        return Response(result)


class UpdateTaskStatusView(APIView):
    def post(self, request, name):
        task = get_object_or_404(models.Task.objects.filter(name=name))
        if task.status != models.Task.ADDED_STATUS:
            return Response(status=HTTP_204_NO_CONTENT)

        stack = builder_api.get_stack(name)
        if stack['status'] == StackStatus.ERROR:
            task.status = models.Task.ERROR_STATUS
            task.error_text = f"Error while building stack: {stack['error_text']}"
        if stack['status'] == StackStatus.PUSHED:
            task.status = models.Task.READY_TO_DEPLOY
        task.save()
        return Response(status=HTTP_204_NO_CONTENT)


# class DeployTaskView(APIView):
#     def post(self, request, name):
#         task = get_object_or_404(models.Task.objects.filter(name=name))
#         if task.status != models.Task.READY_TO_DEPLOY:
#             return Response(f"Can not deploy unready task")
#         deploy_task.delay(task.name)
#         return Response(status=HTTP_204_NO_CONTENT)
