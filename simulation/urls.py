from django.conf.urls import url
from . import views


app_name='simulation'



urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^new/details/$', views.new_details, name='new_details'),
    url(r'^(?P<pk>\d+)/edit/details/$', views.edit_details, name='edit_details'),
    url(r'^(?P<pk>\d+)/edit/data/$', views.edit_data, name='edit_data'),
    url(r'^(?P<pk>\d+)/view_results/$', views.view_results, name='view_results'),
    url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),
]
 
