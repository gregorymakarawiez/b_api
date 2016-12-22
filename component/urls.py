from django.conf.urls import url
from . import views

app_name='component'

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),
]

