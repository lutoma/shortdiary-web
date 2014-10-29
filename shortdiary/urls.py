from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import PostList, PostTimeline, PostDetail, PublicPostDetail, ProfileDetail, PostYearAgo
from django.views.generic import TemplateView
admin.autodiscover()

if settings.DEBUG:
	urlpatterns = patterns('django.views.static',
		url(r'^static/(?P<path>.*)$',  'serve', {'document_root': '/tmp/shortdiary-static/', 'show_indexes': True }),
		url(r'^asset/(?P<path>.*)$',  'serve', {'document_root': '/tmp/shortdiary-asset/', 'show_indexes': True }),
	)
else:
	urlpatterns = patterns('')


api_patterns= format_suffix_patterns(patterns('',
	url(r'^posts/$', PostList.as_view(), name="api-post-list"),
 	url(r'^posts/timeline/$', PostTimeline.as_view(), name='api-post-timeline'),
 	url(r'^posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='api-post-detail'),
 	url(r'^posts/year_ago/$', PostYearAgo.as_view(), name='api-post-yearago'),
 	url(r'^posts/random_public/$', PublicPostDetail.as_view(), name='api-public-post'),
	url(r'^profile/$', ProfileDetail.as_view(), name='api-profile-detail'),
), allowed=["json", "html"])

urlpatterns += patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^i18n/setlang/(?P<language>[a-z]+)/', 'diary.views.switch_language'),

	url(r'^accounts/login/$','django.contrib.auth.views.login',{'template_name':'login.html'}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^accounts/signup/$', 'diary.views.sign_up'),
	url(r'^accounts/settings/$', 'diary.views.account_settings'),

	url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
	url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
	url(r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

	url(r'^accounts/password/change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),

	url(r'^invite/$', 'inviteman.views.invite'),
	url(r'^invite/request/$', 'inviteman.views.invite_request'),

	url(r'^tos/$', TemplateView.as_view(template_name = 'tos.html'), name = 'tos'),
	url(r'^about/$', TemplateView.as_view(template_name = 'about.html'), name = 'about'),

	url(r'^pay/$', TemplateView.as_view(template_name = 'pay.html'), name = 'pay'),
	url(r'^pay/success/$', TemplateView.as_view(template_name = 'pay_success.html'), name = 'pay'),
	url(r'^pay/stripe/$', 'diary.views.pay_stripe_handle'),

	url(r'^posts/new/$', 'diary.views.edit_post'),
	url(r'^posts/(?P<post_id>[0-9]+)/$', 'diary.views.show_post'),
	url(r'^posts/(?P<post_id>[0-9]+)/edit/$', 'diary.views.edit_post'),
	url(r'^posts/(?P<post_id>[0-9]+)/delete/$', 'diary.views.delete_post'),

	url(r'^stats/$', 'diary.views.stats'),
	url(r'^stats/leaderboard/$', 'diary.views.leaderboard'),

	url(r'^explore/$', 'diary.views.explore'),

	url(r'^search/$', 'diary.views.search'),

	url(r'^email/verify/(?P<user_id>[0-9]+)/(?P<hash>[a-z0-9]+)/', 'diary.views.mail_verify'),

	url(r'^db2/$', TemplateView.as_view(template_name = 'db2.html'), name = 'db2'),
	url(r'^/?$', 'diary.views.index'),

	url(r'^api/v1/', include(api_patterns)),
	url(r'^api/v1/oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
)


