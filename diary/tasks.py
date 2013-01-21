# coding: utf-8
import os
import datetime
import mimetypes
from django.utils.translation import ugettext as _
from celery.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import EmailMessage
from diary.models import Post
from django.template.loader import get_template, Context
from django.conf import settings

@periodic_task(run_every = crontab(hour="*", minute="0", day_of_week="*"))
def process_mails():
	print('Sending mails…')

	mail_template = get_template('mails/post.txt')

	# Change to years = 1 in production
	searched_date = datetime.date.today() - datetime.timedelta(days = 7)
	print('Searching mails from {}'.format(searched_date))

	posts = Post.objects.filter(date = searched_date, sent = False)
	print('Found {} mail(s) to send'.format(len(posts)))

	for post in posts:
		print('Sending mail for post #{} ({})'.format(post.id, post))
		
		if not post.author.get_profile().mail_verified:
			print('User hasn\'t verified mail address, skipping')
			continue

		mail = EmailMessage(
				_('Your shortdiary post from {0}').format(post.date),
				mail_template.render(Context({'post': post, 'MEDIA_URL': settings.MEDIA_URL})),
				'shortdiary <team@shortdiary.me>',
				['{0} <{1}>'.format(post.author.username, post.author.email)],
				headers = {'X-Shortdiary-Post-Date': searched_date}
			)

		if post.image and mimetypes.guess_type(post.image.name)[0]):
			mail.attach(
				os.path.split(post.image.name)[1],
				post.image.read(),
				mimetypes.guess_type(post.image.name)[0]
			)

		mail.send()

		post.sent = True
		post.save()
