# coding: utf-8
import os
import datetime
import mimetypes
from django.utils.translation import ugettext as _
from celery.schedules import crontab
from celery.decorators import periodic_task
from diary.models import Post
from django.template.loader import get_template, Context
from django.conf import settings

def process_mails(searched_date):
	print('Sending mails for {0}…'.format(searched_date))

	posts = Post.objects.filter(date = searched_date, sent = False)
	print('Found {} mail(s) to send'.format(len(posts)))

	for post in posts:
		print('Sending mail for post #{} ({})'.format(post.id, post))
		
		if not post.author.mail_verified:
			print('–– User hasn\'t verified email address, skipping')
			continue

		post.send_mail()

@periodic_task(run_every = crontab(hour="0", minute="0", day_of_week="*"))
def process_mails_for_today():
	searched_date = datetime.date.today() - datetime.timedelta(days = 365)
	process_mails(searched_date)