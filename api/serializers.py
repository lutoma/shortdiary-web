from diary.models import Post, DiaryUser
from rest_framework import serializers
import datetime
from django.utils.translation import ugettext as _


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	lastseen = serializers.CharField(source="last_seen_at", read_only=True)

	class Meta:
		model = DiaryUser
		fields = ('id', 'username', 'email', 'mail_verified', 'language', 'lastseen', 'geolocation_enabled')
		read_only_fields = ('username', 'mail_verified')


class PostSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='api-post-detail',
	)
	class Meta:
		model = Post
		fields = ('id', 'url', 'date', 'text', 'mood', 'image', 'location_lat', 'location_lon', 'location_verbose', 'public', 'part_of')

class PublicPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('get_public_text')

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