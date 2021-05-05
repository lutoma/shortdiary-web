from datetime import datetime
from django.utils.timezone import utc


class TrackLastActivityMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		user = request.user

		if user.is_authenticated:
			user.last_seen_at = datetime.utcnow().replace(tzinfo=utc)
			user.save(update_fields=['last_seen_at'])

		return self.get_response(request)
