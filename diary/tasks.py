import datetime
import diary.models
from django.core.cache import cache
from django.core.mail import mail_managers
from django.contrib.humanize.templatetags.humanize import apnumber
from shortdiary.email import send_email
from django.db.models import Count
from guess_language import guess_language
import babel


def process_mails(searched_date):
	print('Sending mails for {0}…'.format(searched_date))

	posts = diary.models.Post.objects.filter(date=searched_date, sent=False)
	print('Found {} mail(s) to send'.format(len(posts)))

	for post in posts:
		print('Sending mail for post #{} ({})'.format(post.id, post))

		if not post.author.mail_verified:
			print('–– User hasn\'t verified email address, skipping')
			continue

		post.send_mail()


def process_mails_for_today():
	searched_date = datetime.date.today() - datetime.timedelta(days=365)
	process_mails(searched_date)


def update_leaderboard():
	streak_leaders = sorted(diary.models.DiaryUser.objects.all(),
		key=lambda t: t.get_streak(), reverse=True)[:10]

	streak_leaders = filter(lambda t: t.get_streak() > 1, streak_leaders)

	posts_leaders = sorted(diary.models.DiaryUser.objects.all(),
		key=lambda t: t.posts.all().count(), reverse=True)[:10]

	posts_leaders = filter(lambda t: t.posts.all().count() > 1, posts_leaders)

	char_leaders = sorted(diary.models.DiaryUser.objects.all(),
		key=lambda t: t.get_post_characters(), reverse=True)[:10]

	char_leaders = filter(lambda t: t.get_post_characters() > 1, char_leaders)

	avg_post_length_leaders = filter(lambda t: t.posts.all().count() > 20,
		diary.models.DiaryUser.objects.all())

	avg_post_length_leaders = sorted(avg_post_length_leaders,
		key=lambda t: t.get_average_post_length(), reverse=True)[:10]

	# This is ugly and should be rewritten at some point to use Post.get_language_name().
	def get_language_name(iso):
		try:
			return babel.Locale(iso).get_display_name('en_US')
		except babel.UnknownLocaleError:
			return ''

	popular_languages = diary.models.Post.objects.filter(natural_language__isnull=False)
	popular_languages = popular_languages.values('natural_language').annotate(
		count=Count('natural_language'))

	popular_languages = filter(lambda t: len(t['natural_language'].strip()) > 0, popular_languages)
	popular_languages = sorted(popular_languages, key=lambda t: t['count'], reverse=True)[:10]
	popular_languages = map(lambda l: {
		'count': l['count'],
		'name': get_language_name(l['natural_language'])
	}, popular_languages)

	popular_locations = diary.models.Post.objects.filter(location_verbose__isnull=False)
	popular_locations = popular_locations.values('location_verbose').annotate(
		count=Count('location_verbose'))

	popular_locations = filter(lambda t: len(t['location_verbose']) > 0, popular_locations)
	popular_locations = sorted(popular_locations, key=lambda t: t['count'], reverse=True)[:10]

	cache.set_many({
		'leaderboard_streak_leaders': list(streak_leaders),
		'leaderboard_posts_leaders': list(posts_leaders),
		'leaderboard_char_leaders': list(char_leaders),
		'leaderboard_avg_post_length_leaders': list(avg_post_length_leaders),
		'leaderboard_popular_languages': list(popular_languages),
		'leaderboard_popular_locations': list(popular_locations),
		'leaderboard_last_update': datetime.datetime.now(),
	})


def update_streak(user):
	"""
	This returns information on how long the "streak" of this user has been
	lasting. Streak in this context means continous posts on following days
	going backwards starting from today or yesterday or the day before.
	"""

	# It probably makes sense to move this function back to models.py

	user_posts = diary.models.Post.objects.filter(author=user).order_by('-date')

	if len(user_posts) == 0:
		return 0

	first_posssible = datetime.date.today() - datetime.timedelta(days=2)
	post = user_posts[0]

	if first_posssible - post.date > datetime.timedelta(days=1):
		return 0

	streak = 0
	for post, previous_post in zip(user_posts, [post] + list(user_posts)):
		if (previous_post.date - post.date) > datetime.timedelta(days=1):
			return streak
		streak += 1

	# This is invalidated as soon as a new post is written, so use a long
	# lifetime. Don't make it infinite though so as to not fill up Redis
	# with timelines of inactive users
	cache.set(f'diary_{user.id}_streak', streak, 2419200)
	return streak


def send_reminder_mail(user):
	"""
	Sends out the mail for this post
	"""

	print('Sending reminder mail to user {}'.format(user.username))

	send_email(user, 'streak-reminder', {
		'streak_length': apnumber(user.get_streak())
	})


def send_reminder_mails():

	# Get all relevant users (Have streak, last post 2 days ago)
	two_days_ago = datetime.date.today() - datetime.timedelta(days=2)
	users = diary.models.DiaryUser.objects.all()
	users = filter(lambda t: t.get_streak() > 0
		and t.posts.order_by('-date')[0].date == two_days_ago, users)

	map(send_reminder_mail, users)


def guess_post_language(post):
	if post.uses_pgp():
		return

	guess = guess_language(post.text)

	if guess == 'UNKNOWN':
		return

	post.natural_language = guess

	# This update_fields part here is crucial since this allows us to filter
	# in the event to avoid recursion, so don't remove it!
	post.save(update_fields=['natural_language'])


def get_users_for_timeframe(**kwargs):
	filter_time = datetime.datetime.now() - datetime.timedelta(**kwargs)
	users = diary.models.DiaryUser.objects.filter(last_seen_at__gte=filter_time)
	return '\n'.join(map(lambda u: u.username, users))


def send_active_users_overview():
	'''
	Sends simple stats of current active users to managers
	'''

	active_24h = get_users_for_timeframe(hours=24)
	active_7d = get_users_for_timeframe(days=7)
	active_30d = get_users_for_timeframe(days=30)

	message = '''
Current active shortdiary users:

Last 24 hours:

{}

Last 7 days:

{}

Last 30 days:

{}
	'''.format(active_24h, active_7d, active_30d)

	mail_managers('Current active users statistics', message)
