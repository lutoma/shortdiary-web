from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.db.models.functions import Length, Coalesce
from django.db.models import Sum, Avg, IntegerField
from django.conf import settings
from django_q.tasks import async_task
from django.core.cache import cache
from django.dispatch import receiver
from shortdiary.email import send_email
from collections import Counter
from functools import reduce
import diary.tasks as tasks
import hashlib
import babel
import datetime
import re


class DiaryUser(AbstractUser):
	last_seen_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Last seen at'))
	email_verified = models.BooleanField(default=False, verbose_name=_('Email verified?'))
	language = models.CharField(default='en_US', max_length=5, verbose_name=_('Language'))

	# Privacy settings
	include_in_leaderboard = models.BooleanField(verbose_name=_('Include in leaderboard'),
		default=True)

	geolocation_enabled = models.BooleanField(verbose_name=_('Post location enabled'), default=True)

	def get_verification_hash(self):
		return hashlib.sha256(self.email.encode('utf-8')
			+ settings.SECRET_KEY.encode('utf-8')).hexdigest()

	def send_verification_mail(self):
		send_email(self, 'email-verification', {'hash': self.get_verification_hash()})

	def get_streak(self):
		cached_streak = cache.get(f'diary_{self.id}_streak')
		if cached_streak:
			return cached_streak
		return tasks.update_streak(self)

	def get_year_history(self):
		"""
		Returns the length of posts for a user for the last 356 days.
		"""

		grid = [None] * 365

		for post in Post.objects.filter(author=self, date__year=datetime.date.today().year):
			grid[post.date.timetuple().tm_yday] = post

		return grid

	def get_post_characters(self):
		return self.posts.aggregate(sum=Coalesce(Sum(Length('text')), 0,
			output_field=IntegerField()))['sum']

	def get_average_post_length(self):
		return self.posts.aggregate(avg=Coalesce(Avg(Length('text')), 0,
			output_field=IntegerField()))['avg']

	def get_mention_toplist(self):
		'''
		Returns the most frequently mentioned nicknames of this user
		'''

		names = list(map(lambda post: post.get_mentions(), self.posts.all()))

		if len(names) < 1:
			return

		names = reduce(lambda names, name: names + name, names)
		names = list(map(lambda name: name[1:].lower(), names))
		return Counter(names).most_common()


class Post(models.Model):
	MENTION_REGEX = re.compile(r'@\w+', re.UNICODE)

	def validate_date(value):
		delta = datetime.date.today() - value
		if delta.days > 4:
			pass
#			raise ValidationError(_('Post date cannot be older than 4 days'))

	author = models.ForeignKey(DiaryUser, verbose_name=_('author'), related_name='posts',
		on_delete=models.CASCADE)

	date = models.DateField(verbose_name=('date'), validators=[validate_date])
	text = models.TextField(verbose_name=_('text'))
	mood = models.IntegerField(verbose_name=_('mood'))
	image = models.ImageField(upload_to='postimages/%d%m%y/', blank=True, verbose_name=_('image'))
	public = models.BooleanField(verbose_name=_('public'), default=False)
	part_of = models.CharField(blank=True, null=True, max_length=600, verbose_name=_('part of'))

	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
	last_changed_at = models.DateTimeField(auto_now=True, verbose_name=_('last changed at'))

	sent = models.BooleanField(default=False, verbose_name=_('mail sent?'))

	location_lat = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True,
		verbose_name=_('Location latitude'))

	location_lon = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True,
		verbose_name=_('Location longitude'))

	location_verbose = models.CharField(max_length=400, blank=True, verbose_name=_('Location name'))

	# FIXME Should not be nullable with blank=True
	natural_language = models.CharField(max_length=5, blank=True, null=True,
		verbose_name=_('Natural language'))

	class Meta:
		verbose_name = _('post')
		verbose_name_plural = _('posts')
		ordering = ['-date']
		unique_together = [['author', 'date']]

	def __str__(self):
		return f'{self.author} on {self.date}'

	def is_editable(self):
		"""
		Should this post still be editable by the user?
		"""

		return (self.date > datetime.date.today() - datetime.timedelta(days=3))

	is_editable.admin_order_field = 'date'
	is_editable.boolean = True
	is_editable.short_description = 'Still editable by user?'

	def get_activity_color(self):
		length = len(self.text)

		if(length <= 50):
			return '#d6e685'

		if(length <= 150):
			return '#8cc665'

		if(length <= 250):
			return '#44a340'

		return '#1e6823'

	def send_mail(self):
		"""
		Sends out the mail for this post
		"""

		# FIXME Might want to attach image if it exists, but probably
		# need to check size for that/do resizing
		send_email(self.author, 'post', {
			'text': self.text,
			'date': self.date.strftime("%B %d, %Y"),
			'post_id': self.id,
			'post_is_public': self.public,
			'post_has_image': self.image is not None,
		})

		self.sent = True
		self.save()

	def get_mentions(self):
		'''
		Get list of people mentioned in this post
		'''

		return self.MENTION_REGEX.findall(self.text)

	def get_public_text(self):
		"""
		The public version of this post's text (i.e. with all names replaced)
		"""

		return self.MENTION_REGEX.sub('███', self.text)

	def uses_pgp(self):
		"""
		If this post makes use of PGP encryption (Used to exclude it from
		language statistics and such)
		"""

		return '-BEGIN PGP MESSAGE-' in self.text

	def get_language_name(self, locale='en_US'):
		verbose_language = _('Unknown')

		if self.natural_language:
			try:
				verbose_language = babel.Locale(self.natural_language).get_display_name(locale)
			except babel.UnknownLocaleError:
				pass
		elif self.uses_pgp():
			verbose_language = _('PGP encrypted')

		return verbose_language


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def update_post_signal(sender, instance, **kwargs):
	async_task('diary.tasks.update_streak', instance.author)

	# Only run the post language guesser if other fields than the natural
	# language were updated. Otherwise, this would result in recursion.
	if not ('update_fields' in kwargs and kwargs['update_fields'] == frozenset(['natural_language'])):
		async_task('diary.tasks.guess_post_language', instance)
