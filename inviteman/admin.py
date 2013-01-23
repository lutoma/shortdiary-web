from inviteman.models import Invite
from django.contrib import admin

class InviteAdmin(admin.ModelAdmin):
	list_display = ['generated_by', 'code']

admin.site.register(Invite, InviteAdmin)