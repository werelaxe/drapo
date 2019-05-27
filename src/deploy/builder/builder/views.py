from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.conf import settings


class MyView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request: Request):
        pass

    def get(self, request: Request):
        return Response({"registry_url": settings.REGISTRY_URL})
