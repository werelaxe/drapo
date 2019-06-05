import os

from django.core.files import File
from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.conf import settings


from . import models
from .celery_tasks import process_filecontext


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
        process_filecontext.delay(new_file_context.id)

        return Response({"filecontext_id": new_file_context.id})


class ContextFileContextsListView(APIView):
    def get(self, request, id):
        if id is None:
            query_set = models.FileContext.objects.all()
        else:
            query_set = models.FileContext.objects.filter(id=id)
        result = []
        for filecontext in query_set:
            prepared_filecontext = model_to_dict(filecontext)
            if not prepared_filecontext['dc_file']:
                prepared_filecontext.pop('dc_file')
            prepared_filecontext.pop('context')
            host = request.META.get('HTTP_HOST')
            prepared_filecontext['download_url'] = host + prepared_filecontext['download_url']
            result.append(prepared_filecontext)
        return Response(result)


class ContextFileDownloadView(APIView):
    def get(self, request, id):
        filecontext = get_object_or_404(models.FileContext.objects.filter(id=id))
        context_filename = models.context_file_path(filecontext, id)
        with open(context_filename, "rb") as file:
            response = HttpResponse(File(file), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{id}.zip"'
            return response
