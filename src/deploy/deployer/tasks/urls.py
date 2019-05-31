from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^(?P<name>[^/]+)?$', views.Task.as_view()),
    url(r'^add/(?P<name>[^/]+)$', views.TaskAddView.as_view()),
    # url(r'^download/(?P<name>[^/]+)$', views.FileDownloadView.as_view()),
    url(r'^filecontexts/upload/(?P<filename>[^/]+)$', views.FileContextUploadView.as_view()),
]
