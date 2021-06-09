# Default settings
# DO NOT MODIFY THIS FILE FOR YOUR LOCAL INSTALLATION.
# Instead, create a file called settings_local.py and override stuff you want to change there.

import os
from datetime import timedelta

SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))

DEBUG = True

ADMINS = (
	('Example Admin', 'shortdiary-admin@example.org'),
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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'asset')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/asset/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static-collect')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'this-is-not-the-production-key'

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = (
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django_otp.middleware.OTPMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'diary.middleware.TrackLastActivityMiddleware'
)

ROOT_URLCONF = 'shortdiary.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'shortdiary.wsgi.application'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates/'],
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'django.template.context_processors.i18n',
			],
			'loaders': [
				'django.template.loaders.filesystem.Loader',
				'django.template.loaders.app_directories.Loader',
			]
		},
	},
]

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	'django.contrib.admin',
	'django_q',
	'corsheaders',
	'rest_framework',
	'django_otp',
	'django_otp.plugins.otp_static',
	'django_otp.plugins.otp_totp',
	'trench',
	'diary',
	'apiv2',
)

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
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated',
	],
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
	)
}


AUTH_USER_MODEL = 'diary.DiaryUser'


TRENCH_AUTH = {
	'SECRET_KEY_LENGTH': 32,
	'APPLICATION_ISSUER_NAME': 'shortdiary',

	'MFA_METHODS': {
		'sms': {
			'VERBOSE_NAME': 'Text message',
			'VALIDITY_PERIOD': 60 * 10,
			'HANDLER': 'trench.backends.twilio.TwilioBackend',
			'SOURCE_FIELD': 'phone_number',
			'TWILIO_ACCOUNT_SID': None,
			'TWILIO_AUTH_TOKEN': None,
			'TWILIO_VERIFIED_FROM_NUMBER': None,
		},
		'app': {
			'VERBOSE_NAME': 'Authenticator app',
			'VALIDITY_PERIOD': 60 * 10,
			'USES_THIRD_PARTY_CLIENT': True,
			'HANDLER': 'trench.backends.application.ApplicationBackend',
		}
	},
}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
	'REFRESH_TOKEN_LIFETIME': timedelta(days=21),
	'ISSUER': 'shortdiary'
}

POSTMARK_KEY = None

HCAPTCHA_SITEKEY = None
HCAPTCHA_SECRET = None


# Use the file local_settings.py to overwrite the defaults with your own settings
try:
	from shortdiary.settings_local import *  # noqa: F403 F401
except ImportError:
	pass
