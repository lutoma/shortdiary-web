# coding: utf-8

from datetime import datetime 
from django.utils.timezone import utc

class TrackLastActivityMiddleware:
	def process_request(self, request):
		user = request.user

		if user.is_authenticated():
			up = user.get_profile()
			up.last_seen_at = datetime.utcnow().replace(tzinfo=utc)
			up.save()
	
		return None