from django.conf.urls import url, include
from django.contrib import admin

from .views import MyView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', MyView.as_view()),
    url(r'^stacks/', include(('stacks.urls', 'stacks'), namespace='stacks')),
]
