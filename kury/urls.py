from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  url(r'^navigation/', include('navigation.urls', namespace='navigation')),
  url(r'^pages/', include('pages.urls', namespace='pages')),
  url(r'^courses/', include('courses.urls', namespace='courses')),
  url(r'^carousel/', include('carousel.urls', namespace='carousel')),
  url(r'^', include('base.urls', namespace='base')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
