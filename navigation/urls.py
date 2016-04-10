from django.conf.urls import url
from . import views

urlpatterns = [
  url(
    r'^admin$',
    views.admin_index,
    name='admin_index'
  ),
  url(
    r'^admin/(?P<pk>[0-9]+)$',
    views.admin_edit,
    name='admin_edit'
  ),
  url(
    r'^admin/(?P<pk>[0-9]+)/delete$',
    views.admin_delete,
    name='admin_delete'
  ),
]
