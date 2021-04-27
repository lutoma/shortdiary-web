from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from diary.models import Post, DiaryUser
from django.db.models import Avg, Count
from django.db.models.functions import Cast, Length
from django.db.models import IntegerField

from .serializers import (
	UserSerializer, PostSerializer, PrivatePostSerializer,
	LeaderboardSerializer
)


class CurrentUserView(APIView):
	def get(self, request):
		serializer = UserSerializer(request.user, context={'request': request})
		return Response(serializer.data)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = PrivatePostSerializer

	# def perform_create(self, serializer):
	# 	serializer.save(author=self.request.user)

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)


class RandomPublicPostView(APIView):
	def get(self, request, format=None):
		post = Post.objects.filter(public=True).order_by('?').first()
		if not post:
			return Response(None, status=status.HTTP_404_NOT_FOUND)

		serializer = PostSerializer(post, context={'request': request})
		return Response(serializer.data)


class LeaderboardView(APIView):
	def get(self, request, format=None):
		users = DiaryUser.objects.all()

		number_of_posts = users.annotate(num_posts=Count('posts')) \
			.filter(num_posts__gt=0) \
			.order_by('-num_posts') \
			.values('username', 'num_posts')[:10]

		average_post_length = users.filter(posts__gt=0) \
			.annotate(avg_length=Cast(Avg(Length('posts__text')), IntegerField())) \
			.order_by('-avg_length') \
			.values('username', 'avg_length')[:10]

		# FIXME Turn this into a DB function… somehow
		streak_leaders = map(lambda x: {'username': x.username, 'streak': x.get_streak()}, users.filter(posts__gt=0))
		streak_leaders = sorted(streak_leaders, key=lambda x: x['streak'])[:10]

		leaderboard = {
			'number_of_posts': number_of_posts,
			'average_post_length': average_post_length,
			'longest_current_streak': streak_leaders
		}

		serializer = LeaderboardSerializer(leaderboard, context={'request': request})
		return Response(serializer.data)
