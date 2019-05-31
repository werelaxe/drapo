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

        models.FileContext.objects.create(
            name=filename,
            context=file_obj,
            download_url='/filecontexts/download/' + filename,
        )
        return Response(status=HTTP_204_NO_CONTENT)


class TaskAddView(APIView):
    def post(self, request: Request, name, format=None):
        if Task.objects.filter(name=name).count():
            return Response('Task already exists', status=400)
        if 'filecontext' not in request.GET:
            return Response("Filecontext id is required as URL parameter", status=400)
        try:
            filecontext_id = request.GET['filecontext'][0]

        except ValueError:
            pass
        return Response(status=200)
