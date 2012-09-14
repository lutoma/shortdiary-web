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
	# Examples:
	# url(r'^$', 'shortdiary.views.home', name='home'),
	# url(r'^shortdiary/', include('shortdiary.foo.urls')),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^i18n/setlang/(?P<language>[a-z]+)', 'diary.views.switch_language'),

	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

	url(r'^post/new/', 'diary.views.new_post'),
	url(r'^post/show/(?P<post_id>[0-9]+)/', 'diary.views.show_post'),
	url(r'^/?$', 'diary.views.index'),
)
