from django.utils.translation import ugettext_lazy as _
from diary.models import Post, DiaryUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


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

	list_display = ['author', 'date', 'public', 'natural_language', 'sent', 'is_editable']
	list_filter = ['sent', 'created_at', 'public', 'natural_language']
	search_fields = ('author__username',)
	date_hierarchy = 'date'


class UserAdmin(DjangoUserAdmin):
	list_display = ['username', 'email', 'last_seen_at', 'language']
	list_filter = ['email_verified', 'last_seen_at', 'geolocation_enabled', 'include_in_leaderboard']
	readonly_fields = ('last_seen_at',)
	date_hierarchy = 'last_seen_at'


admin.site.register(Post, PostAdmin)
admin.site.register(DiaryUser, UserAdmin)
