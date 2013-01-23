from rest_framework import serializers
from inviteman.models import InviteRequest

class InviteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteRequest
        fields = ('email',)