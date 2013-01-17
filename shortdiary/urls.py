from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

if settings.DEBUG:
	urlpatterns = patterns('django.views.static',
		url(r'^static/(?P<path>.*)$',  'serve', {'document_root': '/tmp/shortdiary-static/', 'show_indexes': True }),
		url(r'^asset/(?P<path>.*)$',  'serve', {'document_root': '/tmp/shortdiary-asset/', 'show_indexes': True }),
	)
else:
	urlpatterns = patterns('')

urlpatterns += patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^i18n/setlang/(?P<language>[a-z]+)', 'diary.views.switch_language'),

	url(r'^accounts/login/$', 'diary.views.login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^accounts/signup/$', 'diary.views.sign_up'),
	url(r'^accounts/settings/$', 'diary.views.account_settings'),

	url(r'^invites/new/', 'diary.views.invite'),

	url(r'^tos/', 'diary.views.tos'),
	url(r'^about/', 'diary.views.about'),

	url(r'^posts/new/', 'diary.views.new_post'),
	url(r'^posts/(?P<post_id>[0-9]+)/', 'diary.views.show_post'),
	url(r'^posts/(?P<post_id>[0-9]+)/edit/', 'diary.views.edit_post'),

	url(r'^email/verify/(?P<user_id>[0-9]+)/(?P<hash>[a-z0-9]+)/', 'diary.views.mail_verify'),

	url(r'^/?$', 'diary.views.index'),
)
