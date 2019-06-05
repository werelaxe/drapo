from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    url(r'^filecontexts/', include(('filecontexts.urls', 'filecontexts'), namespace='filecontexts')),
    url(r'^task_instances/', include(('task_instances.urls', 'task_instances'), namespace='task_instances')),
]
