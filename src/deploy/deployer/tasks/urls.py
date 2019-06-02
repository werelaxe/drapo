from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<name>[^/]+)?$', views.TaskListView.as_view()),
    url(r'^add/(?P<name>[^/]+)$', views.TaskAddView.as_view()),
    url(r'^update/(?P<name>[^/]+)$', views.UpdateTaskStatusView.as_view()),

    url(r'^filecontexts/(?P<id>[^/]+)?$', views.ContextFileContextsListView.as_view()),
    url(r'^filecontexts/upload/(?P<filename>[^/]+)$', views.FileContextUploadView.as_view()),
    url(r'^filecontexts/download/(?P<id>[^/]+)$', views.ContextFileDownloadView.as_view()),
]
