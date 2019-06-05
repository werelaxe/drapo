from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<id>[^/]+)?$', views.ContextFileContextsListView.as_view()),
    url(r'^upload/(?P<filename>[^/]+)$', views.FileContextUploadView.as_view()),
    url(r'^download/(?P<id>[^/]+)$', views.ContextFileDownloadView.as_view()),
]
