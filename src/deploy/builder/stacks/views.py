from django.core.files import File
from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework import authentication, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from . import models
from .celery_tasks import process_stack_task
from .stack_processor import check_images


class FileUploadView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        if 'zip' not in file_obj.content_type:
            return Response('HTTP-request must contain a zip-file', status=HTTP_400_BAD_REQUEST)

        stacks = models.Stack.objects.filter(name=filename)
        if stacks.count():
            stack = stacks.first()
            stack.delete()

        models.Stack.objects.create(
            name=filename,
            context=file_obj,
            download_url='/stacks/download/' + filename,
            status=models.Stack.ENQUEUED_STATUS,
        )
        process_stack_task.delay(filename)
        return Response(status=HTTP_204_NO_CONTENT)


class StacksListView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, name):
        if name is None:
            query_set = models.Stack.objects.all()
        else:
            query_set = models.Stack.objects.filter(name=name)
        result = []
        for stack in query_set:
            prepared_stack = model_to_dict(stack)
            if not prepared_stack['config']:
                prepared_stack.pop('config')
            prepared_stack.pop('context')
            host = request.META.get('HTTP_HOST')
            prepared_stack['download_url'] = host + prepared_stack['download_url']
            result.append(prepared_stack)
        return Response(result)


class FileDownloadView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, name):
        context_filename = models.context_file_path(None, name)
        with open(context_filename, "rb") as file:
            response = HttpResponse(File(file), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=""'.format(name)
            return response


class CheckStackView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, name):
        stack = get_object_or_404(models.Stack.objects.filter(name=name))
        if stack.status != models.Stack.PUSHED_STATUS:
            return Response("Checking possible only for pushed stacks", status=HTTP_400_BAD_REQUEST)
        ok = check_images(stack)
        if ok:
            return Response(status=HTTP_204_NO_CONTENT)
        message = f"One of images of stack '{stack.name}' is missed. Stack will be rebuild"

        stack.status = models.Stack.ENQUEUED_STATUS
        stack.error_message = message
        stack.save()
        process_stack_task.delay(stack.name)
        return Response(message)
