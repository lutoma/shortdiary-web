from inviteman.models import Invite, InviteRequest
from django.contrib import admin

class InviteAdmin(admin.ModelAdmin):
	list_display = ['generated_by', 'code']

class InviteRequestAdmin(admin.ModelAdmin):
	list_display = ['email', 'created_at']

admin.site.register(Invite, InviteAdmin)
admin.site.register(InviteRequest, InviteRequestAdmin)