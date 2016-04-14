from django.conf.urls import url
from . import views

urlpatterns = [
  url(
    r'^$',
    views.landing_page,
    name='landing_page'
  ),
  url(
    r'^staff$',
    views.staff,
    name='staff'
  )
]
