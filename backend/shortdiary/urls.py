from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
	path('api/v2/', include('apiv2.urls', namespace='apiv2')),
]

# Serve assets and admin in development. In production the assets should come from
# an external host configured using django-storages, and the admin interface
# should run on a separate internal server (see urls_admin.py)
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += [path('admin/', admin.site.urls)]
