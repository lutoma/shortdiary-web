from diary.models import DiaryUser, Post, PostImage
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
import requests


class UserSerializer(serializers.ModelSerializer):
	posts_avg_chars = serializers.IntegerField(source='get_average_post_length', read_only=True)
	streak = serializers.IntegerField(source='get_streak', read_only=True)
	posts_count = serializers.IntegerField(source='posts.count', read_only=True)
	captcha = serializers.CharField(write_only=True)

	def validate_captcha(self, value):
		try:
			req = requests.post('https://hcaptcha.com/siteverify', data={
				'response': value,
				'secret': settings.HCAPTCHA_SECRET,
				'sitekey': settings.HCAPTCHA_SITEKEY
			})

			req.raise_for_status()
			response = req.json()
			if not response['success']:
				raise ValidationError(f"Captcha verification failed: {', '.join(response['error-codes'])}")

		# Fail open if hcaptcha is down or something
		except requests.exceptions.RequestException:
			pass

	def create(self, validated_data):
		validated_data.pop('captcha', None)
		user = super().create(validated_data)
		user.set_password(validated_data['password'])
		user.save(update_fields=['password'])
		return user

	class Meta:
		model = DiaryUser
		fields = [
			'id',
			'username',
			'email',
			'email_verified',
			'phone_number',
			'language',
			'posts_avg_chars',
			'posts_count',
			'streak',
			'geolocation_enabled',
			'include_in_leaderboard',
			'password',
			'captcha'
		]

		read_only_fields = [
			'id',
			'email_verified',
			'post_avg_chars',
			'posts_count',
			'streak'
		]

		extra_kwargs = {
			'password': {'write_only': True}
		}


class PostImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostImage
		fields = ['id', 'post', 'image', 'thumbnail']
		read_only_fields = ['thumbnail']


class PostSerializer(serializers.ModelSerializer):
	# Must be true since for other people's (public) posts,
	# PublicPostSerializer is used.
	is_own = serializers.ReadOnlyField(default=True)
	images = PostImageSerializer(many=True, read_only=True)
	author = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = Post
		fields = [
			'author',
			'id',
			'is_own',
			'date',
			'text',
			'mood',
			'tags',
			'images',
			'location_lat',
			'location_lon',
			'location_verbose',
			'public',
			'natural_language',
		]

		validators = [
			UniqueTogetherValidator(
				queryset=Post.objects.all(),
				fields=['author', 'date'],
				message='A post for that date already exists'
			)
		]


class FuzzedCoordinateField(serializers.ReadOnlyField):
	"""
	A field that drops significant digits from geo coordinates for privacy
	Returns as strings for consistency with rest of API (DRF returns Decimals
	as strings since JSON only support floats)
	"""

	def to_representation(self, value):
		if not value:
			return None
		return str(round(value, 2))


class PublicPostSerializer(PostSerializer):
	# Technically could be true since this is also used for a user's own posts
	# in the random_public endpoint, but don't bother with that.
	is_own = serializers.ReadOnlyField(default=False)

	text = serializers.CharField(source='get_public_text')
	location_lat = FuzzedCoordinateField()
	location_lon = FuzzedCoordinateField()
	images = PostImageSerializer(many=True, read_only=True)

	class Meta:
		model = Post
		fields = [
			'id',
			'is_own',
			'date',
			'text',
			'mood',
			'images',
			'location_lat',
			'location_lon',
			'location_verbose',
			'public',
			'natural_language'
		]


class LeaderboardSerializer(serializers.Serializer):
	number_of_posts = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))
	average_post_length = serializers.ListField(
		child=serializers.DictField(child=serializers.CharField()))

	longest_current_streak = serializers.ListField(
		child=serializers.DictField(child=serializers.CharField()))

	popular_languages = serializers.ListField(
		child=serializers.DictField(child=serializers.CharField()))

	popular_locations = serializers.ListField(
		child=serializers.DictField(child=serializers.CharField()))

	last_update = serializers.DateTimeField()
