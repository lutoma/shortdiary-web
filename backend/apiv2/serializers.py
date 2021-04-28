from diary.models import DiaryUser, Post
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	post_chars = serializers.CharField(source='get_post_characters')
	posts_avg_chars = serializers.CharField(source='get_average_post_length')
	streak = serializers.CharField(source='get_streak')
	posts_count = serializers.IntegerField(source='posts.count')

	class Meta:
		model = DiaryUser
		fields = [
			'username',
			'email',
			'email_verified',
			'language',
			'is_staff',
			'post_chars',
			'posts_avg_chars',
			'posts_count',
			'streak',
			'geolocation_enabled',
			'include_in_leaderboard'
		]

		read_only_fields = [
			'email_verified',
			'is_staff'
		]


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'date',
			'text',
			'mood',
			'image',
			'location_lat',
			'location_lon',
			'location_verbose',
			'public',
			'part_of',
			'natural_language',
			'is_editable'
		]


class PublicPostSerializer(PostSerializer):
	# Like PostSerializer, but with public_text only
	public_text = serializers.CharField(source='get_public_text')

	class Meta:
		model = Post
		fields = [
			'id',
			'date',
			'public_text',
			'mood',
			'image',
			'location_lat',
			'location_lon',
			'location_verbose',
			'public',
			'part_of',
			'natural_language',
			'is_editable'
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
