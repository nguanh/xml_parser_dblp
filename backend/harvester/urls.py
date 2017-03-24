from django.conf.urls import url

from . import views
#der namespace
app_name = 'Harvester'


urlpatterns = [
    url(r'^config/(?P<config_id>[0-9]+)/log/$', views.log, name='config_log'),
]
