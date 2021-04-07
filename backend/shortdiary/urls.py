from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView
from two_factor.urls import urlpatterns as tf_urls

#from two_factor.urls import urlpatterns as tf_urls
#from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls

from apiv1.views import (
	PostList, PostTimeline, PostDetail, PublicPostDetail, ProfileDetail, PostYearAgo
)

from diary.views import (
	switch_language, sign_up, account_settings, edit_post, show_post,
	delete_post, stats, leaderboard, explore, search, mail_verify,
	index
)

from django.contrib.auth.views import (
	LogoutView, PasswordResetView, PasswordResetDoneView,
	PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,
	PasswordChangeDoneView
)

api_patterns = format_suffix_patterns([
	url(r'^posts/$', PostList.as_view(), name="apiv1-post-list"),
	url(r'^posts/timeline/$', PostTimeline.as_view(), name='apiv1-post-timeline'),
	url(r'^posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='apiv1-post-detail'),
	url(r'^posts/year_ago/$', PostYearAgo.as_view(), name='apiv1-post-yearago'),
	url(r'^posts/random_public/$', PublicPostDetail.as_view(), name='apiv1-public-post'),
	url(r'^profile/$', ProfileDetail.as_view(), name='apiv1-profile-detail'),
], allowed=["json", "html"])


diary_urls = [
	path('tos/', TemplateView.as_view(template_name='tos.html'), name='tos'),
	path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
	path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

	path('posts/new/', edit_post, name='new'),
	url(r'^posts/(?P<post_id>[0-9]+)/$', show_post, name='post_show'),
	url(r'^posts/(?P<post_id>[0-9]+)/edit/$', edit_post, name='post_edit'),
	url(r'^posts/(?P<post_id>[0-9]+)/delete/$', delete_post, name='post_delete'),

	url(r'^stats/$', stats, name='stats'),
	url(r'^stats/leaderboard/$', leaderboard, name='leaderboard'),

	url(r'^explore/$', explore, name='explore'),
	url(r'^search/$', search, name='search'),
	url(r'^email/verify/(?P<user_id>[0-9]+)/(?P<hash>[a-z0-9]+)/', mail_verify, name='email_verify'),

	url(r'^accounts/logout/$', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
	url(r'^accounts/signup/$', sign_up, name='sign_up'),
	url(r'^accounts/settings/$', account_settings, name='account_settings'),

	url(r'^i18n/setlang/(?P<language>[a-z]+)/', switch_language, name='switch_language'),

	url(r'^$', index),
]

urlpatterns = [
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	path('admin/', admin.site.urls),

	url(r'^accounts/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
	url(r'^accounts/password/reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
	url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

	url(r'^accounts/password/reset/complete/$', PasswordResetCompleteView.as_view(),
		name='password_reset_complete'),

	url(r'^accounts/password/change/$', PasswordChangeView, name='password_change'),
	url(r'^accounts/password/change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),

	path('', include(diary_urls)),

	path('api/v1/', include(api_patterns)),
	path('api/v2/', include('apiv2.urls')),
#	url(r'^api/v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
#	url(r'', include(tf_urls, 'two_factor')),
#	url(r'', include(tf_twilio_urls, 'two_factor')),
	path('', include(tf_urls)),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
