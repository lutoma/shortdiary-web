# The URL configuration used by the admin server. This only contains the Django
# admin backend and a static file server for admin CSS files

from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

urlpatterns = [
	path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
	path('', admin.site.urls)
]
