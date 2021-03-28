# coding: utf-8

from datetime import datetime
from django.utils.timezone import utc

class TrackLastActivityMiddleware:
	def process_request(self, request):
		user = request.user

		if user.is_authenticated:
			user.last_seen_at = datetime.utcnow().replace(tzinfo=utc)
			user.save()

		return None
