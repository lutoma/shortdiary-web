# coding: utf-8
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, verbose_name = _('author'))
	date = models.DateField(verbose_name = ('date'))
	text = models.TextField(max_length = 350, verbose_name = _('text'))
	mood = models.CharField(max_length = 100, verbose_name = _('mood'))
	image = models.ImageField(upload_to = 'postimages/%d%m%y/', verbose_name = _('image'))

	created_at = models.DateTimeField(auto_now_add = True)
	last_changed_at = models.DateTimeField(auto_now = True)
