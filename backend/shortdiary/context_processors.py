from django.conf import settings


def debug(request):
	return {'debug': getattr(settings, 'DEBUG', False)}
