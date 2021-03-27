from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView
from two_factor.urls import urlpatterns as tf_urls
from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
from django.views.static import serve

from api.views import (
	PostList, PostTimeline, PostDetail, PublicPostDetail, ProfileDetail, PostYearAgo
)

from diary.views import (
	switch_language, sign_up, account_settings, pay_stripe_handle, edit_post,
	show_post, delete_post, stats, leaderboard, explore, search, mail_verify,
	index
)

from django.contrib.auth.views import (
	logout, password_reset, password_reset_done, password_reset_confirm,
	password_reset_complete, password_change, password_change_done
)

admin.autodiscover()

if settings.DEBUG:
	urlpatterns = [
		url(r'^static/(?P<path>.*)$', serve, {'document_root': '/tmp/shortdiary-static/',
			'show_indexes': True}),

		url(r'^asset/(?P<path>.*)$', serve, {'document_root': '/tmp/shortdiary-asset/',
			'show_indexes': True}),
	]
else:
	urlpatterns = []


api_patterns = format_suffix_patterns([
	url(r'^posts/$', PostList.as_view(), name="api-post-list"),
	url(r'^posts/timeline/$', PostTimeline.as_view(), name='api-post-timeline'),
	url(r'^posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='api-post-detail'),
	url(r'^posts/year_ago/$', PostYearAgo.as_view(), name='api-post-yearago'),
	url(r'^posts/random_public/$', PublicPostDetail.as_view(), name='api-public-post'),
	url(r'^profile/$', ProfileDetail.as_view(), name='api-profile-detail'),
], allowed=["json", "html"])


diary_urls = [
	url(r'^tos/$', TemplateView.as_view(template_name='tos.html'), name='tos'),
	url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

	url(r'^vip/$', TemplateView.as_view(template_name='pay.html'), name='pay'),
	url(r'^pay/success/$', TemplateView.as_view(template_name='pay_success.html'), name='pay'),
	url(r'^pay/stripe/$', pay_stripe_handle, name='stripe'),

	url(r'^posts/new/$', edit_post, name='new'),
	url(r'^posts/(?P<post_id>[0-9]+)/$', show_post, name='post_show'),
	url(r'^posts/(?P<post_id>[0-9]+)/edit/$', edit_post, name='post_edit'),
	url(r'^posts/(?P<post_id>[0-9]+)/delete/$', delete_post, name='post_delete'),

	url(r'^stats/$', stats, name='stats'),
	url(r'^stats/leaderboard/$', leaderboard, name='leaderboard'),

	url(r'^explore/$', explore, name='explore'),
	url(r'^search/$', search, name='search'),
	url(r'^email/verify/(?P<user_id>[0-9]+)/(?P<hash>[a-z0-9]+)/', mail_verify, name='email_verify'),

	url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
	url(r'^accounts/signup/$', sign_up, name='sign_up'),
	url(r'^accounts/settings/$', account_settings, name='account_settings'),

	url(r'^i18n/setlang/(?P<language>[a-z]+)/', switch_language, name='switch_language'),

	url(r'^$', index),
]

urlpatterns += [
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^accounts/password/reset/$', password_reset, name='password_reset'),
	url(r'^accounts/password/reset/done/$', password_reset_done, name='password_reset_done'),
	url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		password_reset_confirm, name='password_reset_confirm'),

	url(r'^accounts/password/reset/complete/$', password_reset_complete,
		name='password_reset_complete'),

	url(r'^accounts/password/change/$', password_change, name='password_change'),
	url(r'^accounts/password/change/done/$', password_change_done, name='password_change_done'),

	url('', include(diary_urls, 'diary')),

	url(r'^api/v1/', include(api_patterns)),
#	url(r'^api/v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
	url(r'', include(tf_urls, 'two_factor')),
	url(r'', include(tf_twilio_urls, 'two_factor')),
]
