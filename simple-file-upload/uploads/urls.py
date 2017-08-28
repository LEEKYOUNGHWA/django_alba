from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploads.core import views


urlpatterns = [
    url(r'^$', views.home, name='main_page'),
    url(r'^(?P<document_id>[0-9]+)/$', views.select, name='pick'),
    url(r'^contact', views.contact, name='contact_page'),
    # url(r'^upload', views.model_form_upload, name='upload'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
