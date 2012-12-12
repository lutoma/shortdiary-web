# coding: utf-8
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
	'''The extended user profile'''

	user = models.OneToOneField(User)
	public = models.BooleanField(verbose_name = _('public'))

	__unicode__ = lambda self: self.user.username

# Automatically create a new user profile when a new user is added
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Post(models.Model):
	author = models.ForeignKey(User, verbose_name = _('author'))
	date = models.DateField(verbose_name = ('date'))
	text = models.TextField(max_length = 350, verbose_name = _('text'))
	mood = models.CharField(max_length = 100, verbose_name = _('mood'))
	image = models.ImageField(upload_to = 'postimages/%d%m%y/', blank = True, verbose_name = _('image'))

	created_at = models.DateTimeField(auto_now_add = True)
	last_changed_at = models.DateTimeField(auto_now = True)

	sent = models.BooleanField(default = False, verbose_name = _('mail sent?'))

	__unicode__ = lambda self: _('{0} at {1}').format(self.author, self.date)