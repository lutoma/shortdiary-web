# These settings are used to run the admin interface on different port than the
# API. The only differnce is the separate URL configuration which contains only
# the admin (which the regular URL config does not have).

# This can be run using an environment variable when launching a WSGI server:
# DJANGO_SETTINGS_MODULE=shortdiary.settings_admin

from .settings import *  # noqa: F403 F401
ROOT_URLCONF = 'shortdiary.urls_admin'
