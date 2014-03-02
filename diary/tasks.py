# coding: utf-8
import os
import datetime
import mimetypes
from django.utils.translation import ugettext as _
from celery.schedules import crontab
from celery.decorators import periodic_task, task
import diary.models
from django.template.loader import get_template, Context
from django.conf import settings
from django.core.cache import cache

def process_mails(searched_date):
	print('Sending mails for {0}…'.format(searched_date))

	posts = diary.models.Post.objects.filter(date = searched_date, sent = False)
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

@periodic_task(run_every = crontab(hour="*", minute="*/5", day_of_week="*"))
def update_leaderboard():
	streak_leaders = sorted(diary.models.DiaryUser.objects.all(), key = lambda t: t.get_streak(), reverse = True)[:10]
	streak_leaders = filter(lambda t: t.get_streak() > 1, streak_leaders)

	posts_leaders = sorted(diary.models.DiaryUser.objects.all(), key = lambda t: t.post_set.all().count(), reverse = True)[:10]
	posts_leaders = filter(lambda t: t.post_set.all().count() > 1, posts_leaders)

	char_leaders = sorted(diary.models.DiaryUser.objects.all(), key = lambda t: t.get_post_characters(), reverse = True)[:10]
	char_leaders = filter(lambda t: t.get_post_characters() > 1, posts_leaders)

	avg_post_length_leaders = sorted(diary.models.DiaryUser.objects.all(),
		key = lambda t: t.get_average_post_length(), reverse = True)[:10]
	avg_post_length_leaders = filter(lambda t: t.get_average_post_length() > 1, posts_leaders)

	cache.set_many({
		'leaderboard_streak_leaders': streak_leaders,
		'leaderboard_posts_leaders': posts_leaders,
		'leaderboard_char_leaders': char_leaders,
		'leaderboard_avg_post_length_leaders': avg_post_length_leaders,
		'leaderboard_last_update': datetime.datetime.now(),
	})

@task
def update_streak(user):
	"""
	This returns information on how long the "streak" of this user has been
	lasting. Streak in this context means continous posts on following days
	going backwards starting from today or yesterday or the day before.
	"""
	user_posts = diary.models.Post.objects.filter(author = user).order_by('-date')

	if len(user_posts) == 0:
		return 0

	first_posssible = datetime.date.today() - datetime.timedelta(days = 2)
	post = user_posts[0]

	if first_posssible - post.date > datetime.timedelta(days = 1):
		return 0

	streak = 0
	for post, previous_post in zip(user_posts, [post] + list(user_posts)):
		if (previous_post.date - post.date) > datetime.timedelta(days = 1):
			return streak
		streak += 1

	return streak
