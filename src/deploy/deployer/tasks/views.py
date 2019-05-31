from django.core import serializers
from django.core.files import File
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from . import models


class FileContextUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        if 'zip' not in file_obj.content_type:
            return Response('HTTP-request must contain a zip-file', status=HTTP_400_BAD_REQUEST)

        new_file_context = models.FileContext.objects.create(
            name=filename,
        )
        new_file_context.context = file_obj
        new_file_context.download_url = f'/filecontexts/download/{new_file_context.id}'
        new_file_context.save()
        return Response(status=HTTP_204_NO_CONTENT)


class TaskAddView(APIView):
    def post(self, request: Request, name, format=None):
        if models.Task.objects.filter(name=name).count():
            return Response(f"Task '{name}' already exists", status=400)
        if 'filecontext' not in request.GET:
            return Response("Filecontext id is required as URL parameter", status=400)
        filecontext_id = request.GET['filecontext'][0]
        file_context = models.FileContext.objects.get(id=filecontext_id)
        models.Task.objects.create(
            name=name,
            status=models.Task.ADDED_STATUS,
            filecontext=file_context,
        )
        return Response(status=HTTP_204_NO_CONTENT)


class ContextFileContextsListView(APIView):
    def get(self, request, id):
        if id is None:
            query_set = models.FileContext.objects.all()
        else:
            query_set = models.FileContext.objects.filter(id=id)
        result = []
        for filecontext in query_set:
            prepared_filecontext = model_to_dict(filecontext)
            prepared_filecontext.pop('context')
            host = request.META.get('HTTP_HOST')
            prepared_filecontext['download_url'] = host + prepared_filecontext['download_url']
            result.append(prepared_filecontext)
        return Response(result)


class ContextFileDownloadView(APIView):
    def get(self, request, id):
        context_filename = models.context_file_path(None, id)
        with open(context_filename, "rb") as file:
            response = HttpResponse(File(file), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{id}.zip"'
            return response
