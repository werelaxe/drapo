from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<name>[^/]+)?$', views.StacksListView.as_view()),
    url(r'^upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    url(r'^download/(?P<name>[^/]+)$', views.FileDownloadView.as_view()),
    url(r'^check/(?P<name>[^/]+)$', views.CheckStackView.as_view()),
]
