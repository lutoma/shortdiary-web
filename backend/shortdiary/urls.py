from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls

#from two_factor.urls import urlpatterns as tf_urls
#from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls

from django.contrib.auth.views import (
	PasswordResetView, PasswordResetDoneView,
	PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,
	PasswordChangeDoneView
)

urlpatterns = [
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	path('admin/', admin.site.urls),

	url(r'^accounts/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
	url(r'^accounts/password/reset/done/$', PasswordResetDoneView.as_view(),
		name='password_reset_done'),

	url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

	url(r'^accounts/password/reset/complete/$', PasswordResetCompleteView.as_view(),
		name='password_reset_complete'),

	url(r'^accounts/password/change/$', PasswordChangeView, name='password_change'),
	url(r'^accounts/password/change/done/$', PasswordChangeDoneView.as_view(),
		name='password_change_done'),

	path('api/v2/', include('apiv2.urls', namespace='apiv2')),
#	url(r'^api/v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
#	url(r'', include(tf_urls, 'two_factor')),
#	url(r'', include(tf_twilio_urls, 'two_factor')),
	path('', include(tf_urls)),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
