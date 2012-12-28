# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from diary.models import Post, UserProfile, Invite
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	# Hide text, mood and image so that they have to manually be collapsed.
	# This allows admins to debug/edit posts without having to see private
	# user data.

	fieldsets = [
		(None, {'fields': ['author', 'date', 'sent']}),
		(
			_('Privacy section. Only open if absolutely needed (Mood, Text, Image)'),
			{'fields': ['mood', 'text', 'image'], 'classes': ['collapse']}
		),
	]

	list_display = ['author', 'date', 'sent']
	list_filter = ['sent', 'created_at']

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'public', 'mail_verified', 'last_seen_at', 'invited_by', 'language']
	list_filter = ['public', 'mail_verified']
	readonly_fields=('last_seen_at',)

class InviteAdmin(admin.ModelAdmin):
    list_display = ['generated_by', 'code']

admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Invite, InviteAdmin)