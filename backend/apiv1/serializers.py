from diary.models import Post, DiaryUser
from rest_framework import serializers
import datetime
from django.utils.translation import ugettext as _


class ProfileSerializer(serializers.ModelSerializer):
	lastseen = serializers.CharField(source="last_seen_at", read_only=True)

	class Meta:
		model = DiaryUser
		fields = ('id', 'username', 'email', 'email_verified', 'language', 'lastseen', 'geolocation_enabled')
		read_only_fields = ('username', 'email_verified')


class PostSerializer(serializers.ModelSerializer):
#	url = serializers.HyperlinkedIdentityField(
#		view_name='api-post-detail',
#	)

	public_text = serializers.SerializerMethodField('get_public_text')
	get_public_text = lambda self, obj: obj.get_public_text()

	class Meta:
		model = Post
		fields = ('id', 'date', 'text', 'public_text', 'mood', 'image', 'location_lat', 'location_lon', 'location_verbose', 'public', 'part_of', 'natural_language')

class PublicPostSerializer(serializers.ModelSerializer):
#	url = serializers.HyperlinkedIdentityField(
#		view_name='api-post-detail',
#	)

	public_text = serializers.SerializerMethodField('get_public_text')
	get_public_text = lambda self, obj: obj.get_public_text()

	class Meta:
		model = Post
		fields = ('id', 'date', 'image', 'location_lat', 'location_lon', 'location_verbose', 'public', 'public_text', 'natural_language')

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post

	def validate_date(self, attrs, source):
		value = attrs[source]
		today = datetime.date.today()
		if (today - value).days > 1:
			raise serializers.ValidationError(_("Invalid date. You can't go that far back."))
		check_post = Post.objects.filter(author = attrs["author"], date = value)
		if len(check_post) != 0:
			raise serializers.ValidationError(_("Invalid date. There already is a post for this date"))
		return attrs
