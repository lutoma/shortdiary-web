from diary.models import DiaryUser, Post, PostImage
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	posts_avg_chars = serializers.IntegerField(source='get_average_post_length', read_only=True)
	streak = serializers.IntegerField(source='get_streak', read_only=True)
	posts_count = serializers.IntegerField(source='posts.count', read_only=True)

	class Meta:
		model = DiaryUser
		fields = [
			'username',
			'email',
			'email_verified',
			'phone_number',
			'language',
			'posts_avg_chars',
			'posts_count',
			'streak',
			'geolocation_enabled',
			'include_in_leaderboard'
		]

		read_only_fields = [
			'email_verified',
			'post_avg_chars',
			'posts_count'
			'streak'
		]


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
			'part_of',
			'natural_language',
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
