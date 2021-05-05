from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v2/', include('apiv2.urls', namespace='apiv2')),
	path('', include(tf_urls)),
]

# The only static files we have are the ones in the Django admin, and for those
# the built-in static file server is good enough.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve assets in development. In production they should come from an external
# host configured using django-storages.
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
