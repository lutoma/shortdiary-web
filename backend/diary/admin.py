from django.utils.translation import ugettext_lazy as _
from diary.models import Post, PostImage, DiaryUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class PostImageInline(admin.TabularInline):
	model = PostImage
	extra = 0


class PostAdmin(admin.ModelAdmin):
	# Hide text, mood and image so that they have to manually be collapsed.
	# This allows admins to debug/edit posts without having to see private
	# user data.

	fieldsets = [
		(None, {'fields': ['author', 'date', 'sent', 'public', 'natural_language']}),
		(
			_('Private section'),
			{'fields': [
				'mood',
				'text',
				'part_of',
				'location_verbose',
				'location_lat',
				'location_lon'
			], 'classes': ['collapse']}
		),
	]

	inlines = [PostImageInline]
	list_display = ['author', 'date', 'public', 'natural_language', 'sent']
	list_filter = ['sent', 'created_at', 'public', 'natural_language']
	search_fields = ('author__username',)
	date_hierarchy = 'date'


class UserAdmin(DjangoUserAdmin):
	fieldsets = [
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
		(
			'Permissions',
			{'fields': (
				'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
			)}
		),

		('Important dates', {'fields': ('last_seen_at', 'last_login', 'date_joined')})
	]

	list_display = ['username', 'email', 'last_seen_at', 'language']
	list_filter = ['email_verified', 'last_seen_at', 'geolocation_enabled', 'include_in_leaderboard']
	readonly_fields = ('last_seen_at', 'last_login', 'date_joined')
	date_hierarchy = 'last_seen_at'


admin.site.register(Post, PostAdmin)
admin.site.register(DiaryUser, UserAdmin)
