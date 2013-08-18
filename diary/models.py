# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.template.loader import get_template, Context
from django.conf import settings
import hashlib
import datetime

class UserProfile(models.Model):
	"""
	The extended user profile
	"""

	user = models.OneToOneField(User)
	public = models.BooleanField(verbose_name = _('public'))
	invited_by = models.ForeignKey(User, related_name = 'user_invited_by', blank = True, null = True, verbose_name = _('invited by'))
	invites_left = models.IntegerField(default = 5, verbose_name = _('invites left'))
	last_seen_at = models.DateTimeField(blank = True, null = True, verbose_name = _('last seen at'))
	mail_verified = models.BooleanField(default = False, verbose_name = _('email verified?'))
	language = models.CharField(default = 'en_US', max_length = 5, verbose_name = _('language'))

	__unicode__ = lambda self: self.user.username

	class Meta:
		verbose_name = _('user profile')
		verbose_name_plural = _('user profiles')

	get_verification_hash = lambda self: hashlib.sha256(self.user.email.encode('utf-8') + settings.SECRET_KEY).hexdigest()

	def send_verification_mail(self):
		mail_template = get_template('mails/verification.txt')
		mail = EmailMessage(
			_('Please verify your email address on shortdiary, {0}'.format(self.user.username)),
			mail_template.render(Context({'mailuser': self.user, 'hash': self.get_verification_hash()})),
			'shortdiary <team@shortdiary.me>',
			['{0} <{1}>'.format(self.user.username, self.user.email)])
		mail.send()

	def get_streak(self):
		# FIXME This code is horrible
		i = 0
		while True:
			try:
				Post.objects.get(author = self, date = datetime.date.today() - datetime.timedelta(days = i + 1))
			except Post.DoesNotExist:
				break
			i += 1

		if Post.objects.get(author = self, date = datetime.date.today()):
			i += 1

		return i

# Automatically create a new user profile when a new user is added
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(create_user_profile, sender=User)

class Post(models.Model):
	"""
	A diary post
	"""

	author = models.ForeignKey(User, verbose_name = _('author'))
	date = models.DateField(verbose_name = ('date'))
	text = models.TextField(max_length = 350, verbose_name = _('text'))
	mood = models.IntegerField(verbose_name = _ ('mood'))
	image = models.ImageField(upload_to = 'postimages/%d%m%y/', blank = True, verbose_name = _('image'))

	created_at = models.DateTimeField(auto_now_add = True, verbose_name = _('created at'))
	last_changed_at = models.DateTimeField(auto_now = True, verbose_name = _('last changed at'))

	sent = models.BooleanField(default = False, verbose_name = _('mail sent?'))

	location_lat = models.DecimalField(max_digits=10, decimal_places=6, blank = True, null = True, verbose_name = _('Location latitude'))
	location_lon = models.DecimalField(max_digits=10, decimal_places=6, blank = True, null = True, verbose_name = _('Location longitude'))
	location_verbose = models.CharField(max_length = 400, blank = True, verbose_name = _('Location name'))

	__unicode__ = lambda self: _('{0} at {1}').format(self.author, self.date)

	class Meta:
		verbose_name = _('post')
		verbose_name_plural = _('posts')

	def get_user_id(self):
		"""
		Get user specific post ID (Aka: The how-manieth post of this user is this?)
		"""
		return len(Post.objects.filter(author = self.author, date__lt = self.date)) + 1

	get_user_id.admin_order_field = 'date'
	get_user_id.boolean = False
	get_user_id.short_description = 'User post ID'

	def is_editable(self):
		"""
		Should this post still be editable by the user?
		"""

		return (self.date > datetime.date.today() - datetime.timedelta(days = 3))

	is_editable.admin_order_field = 'date'
	is_editable.boolean = True
	is_editable.short_description = 'Still editable by user?'
