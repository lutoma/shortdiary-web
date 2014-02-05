# Sample settings for local installation.
# Production settings are different

import os

SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Lukas Martini', 'hello@lutoma.org'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'development.db',					  # Or path to database file if using sqlite3.
		'USER': '',					  # Not used with sqlite3.
		'PASSWORD': '',				  # Not used with sqlite3.
		'HOST': '',					  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',					  # Set to empty string for default. Not used with sqlite3.
	}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'shortdiary-main'
    }
}

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('eo', 'Esperanto'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/tmp/shortdiary-asset/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/asset/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/tmp/shortdiary-static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	os.path.join(SITE_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '38wok0-b&amp;0r31$+m4)24#)vrt(_$84mfi*2gqooc#*x3%-xop9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
#	'htmlmin.middleware.HtmlMinifyMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'diary.middleware.TrackLastActivityMiddleware'
)

debug_context = lambda request: {'DEBUG': DEBUG}

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.request',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.tz',
	'django.contrib.messages.context_processors.messages',
	'shortdiary.settings.debug_context',
)

ROOT_URLCONF = 'shortdiary.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'shortdiary.wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)

GRAVATAR_URL_PREFIX = 'https://secure.gravatar.com/'
GRAVATAR_DEFAULT_IMAGE = 'mm'

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	'south',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'kombu.transport.django',
	'djcelery',
	'django_gravatar',
	'rest_framework',
	'email_extras',
	'diary',
	'inviteman',
	'provider',
    'provider.oauth2',
)

# Asynchronous jobs
BROKER_URL = "django://"
import djcelery
djcelery.setup_loader()

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTH_PROFILE_MODULE = 'diary.UserProfile'

# Cache busting
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.IsOwner',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
    	'rest_framework.authentication.OAuth2Authentication',
    	'rest_framework.authentication.SessionAuthentication',
	),
}

AUTH_USER_MODEL = 'diary.DiaryUser'

# Use the file local_settings.py to overwrite the defaults with your own settings
try:
	from local_settings import *
except ImportError:
	pass

