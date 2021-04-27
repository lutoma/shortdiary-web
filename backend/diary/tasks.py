import datetime
import diary.models
from django.core.cache import cache
from django.core.mail import mail_managers
from django.contrib.humanize.templatetags.humanize import apnumber
from shortdiary.email import send_email
from guess_language import guess_language


def process_mails(searched_date):
	print('Sending mails for {0}…'.format(searched_date))

	posts = diary.models.Post.objects.filter(date=searched_date, sent=False)
	print('Found {} mail(s) to send'.format(len(posts)))

	for post in posts:
		print('Sending mail for post #{} ({})'.format(post.id, post))

		if not post.author.email_verified:
			print('–– User hasn\'t verified email address, skipping')
			continue

		post.send_mail()


def process_mails_for_today():
	searched_date = datetime.date.today() - datetime.timedelta(days=365)
	process_mails(searched_date)


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
