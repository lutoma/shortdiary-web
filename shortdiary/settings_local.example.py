# Sample production settings

DEBUG = False

ADMINS = (
	('Admin Admin', 'hello@example.org'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'shortdiary',
		'USER': 'shortdiary',
		'PORT': '',
		'HOST': 'db-1',
		'PASSWORD': '',
	}
}

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
ALLOWED_HOSTS = ['shortdiary.example.org']

CACHES = {
	'default': {
		'BACKEND': 'django_redis.cache.RedisCache',

		# /1 as database 0 is already used by Django-Q
		'LOCATION': 'redis://127.0.0.1:6379/1',
		'OPTIONS': {
			'CLIENT_CLASS': 'django_redis.client.DefaultClient',
		}
	}
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

SECRET_KEY = ''

# Email settings
POSTMARK_KEY = ''

# Only used for Django admin emails, rest uses Postmark API
DEFAULT_FROM_EMAIL = 'shortdiary <yourfriends@example.org>'
SERVER_EMAIL = 'mail@example.org'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.postmarkapp.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

# For two-factor text messages/calls
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_CALLER_ID = ''
