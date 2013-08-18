from django.contrib.auth.models import User
from diary.models import Post
from rest_framework import serializers
import datetime
from django.utils.translation import ugettext as _


class PostSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='api-post-detail',
	)
	class Meta:
		model = Post
		fields = ('url', 'date', 'text', 'mood', 'image')

class PublicPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('text',)

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
