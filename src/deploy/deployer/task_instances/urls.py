from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add$', views.TaskInstanceAddView.as_view()),
    url(r'^(?P<id>[^/]+)?$', views.TaskInstanceListView.as_view()),
    url(r'^deploy/(?P<id>[^/]+)$', views.TaskInstanceDeployView.as_view()),
    url(r'^undeploy/(?P<id>[^/]+)$', views.TaskInstanceUndeployView.as_view()),
    url(r'^get_addresses/(?P<id>[^/]+)$', views.GetTaskInstanceAddressesView.as_view()),
]
