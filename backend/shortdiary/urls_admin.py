# The URL configuration used by the admin server. This only contains the Django
# admin backend and a static file server for admin CSS files

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
	path('', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
