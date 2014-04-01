# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from diary.models import Post, DiaryUser
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	# Hide text, mood and image so that they have to manually be collapsed.
	# This allows admins to debug/edit posts without having to see private
	# user data.

	fieldsets = [
		(None, {'fields': ['author', 'date', 'sent', 'public', 'natural_language']}),
		(
			_('Privacy section. Only open if absolutely needed (Mood, Text, Image)'),
			{'fields': [
				'mood',
				'text',
				'part_of',
				'image',
				'location_verbose',
				'location_lat',
				'location_lon'
			], 'classes': ['collapse']}
		),
	]

	list_display = ['author', 'date', 'public', 'sent', 'is_editable']
	list_filter = ['sent', 'created_at']
	date_hierarchy = 'date'

class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'email', 'last_seen_at', 'invited_by', 'language']
	list_filter = ['mail_verified', 'last_seen_at', 'geolocation_enabled']
	readonly_fields=('last_seen_at',)
	date_hierarchy = 'last_seen_at'
	search_fields = ('username',)

admin.site.register(Post, PostAdmin)
admin.site.register(DiaryUser, UserAdmin)
