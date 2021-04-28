from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework import viewsets
from diary.models import Post
from django.core.cache import cache


from .serializers import (
	UserSerializer, PostSerializer, PublicPostSerializer,
	LeaderboardSerializer
)


class CurrentUserView(RetrieveUpdateAPIView):
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)


class RandomPublicPostView(RetrieveAPIView):
	serializer_class = PublicPostSerializer

	def get_object(self):
		return Post.objects.filter(public=True).order_by('?').first()


class LeaderboardView(RetrieveAPIView):
	serializer_class = LeaderboardSerializer

	def get_object(self):
		return cache.get('leaderboard')
