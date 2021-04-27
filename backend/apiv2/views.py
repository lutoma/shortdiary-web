from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from diary.models import Post
from django.core.cache import cache


from .serializers import (
	UserSerializer, PostSerializer, PrivatePostSerializer,
	LeaderboardSerializer
)


class CurrentUserView(APIView):
	def get(self, request):
		serializer = UserSerializer(request.user, context={'request': request})
		return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)


class RandomPublicPostView(APIView):
	def get(self, request, format=None):
		post = Post.objects.filter(public=True).order_by('?').first()
		if not post:
			return Response(None, status=status.HTTP_404_NOT_FOUND)

		serializer = PublicPostSerializer(post, context={'request': request})
		return Response(serializer.data)


class LeaderboardView(APIView):
	def get(self, request, format=None):
		leaderboard = cache.get('leaderboard')
		if not leaderboard:
			return Response(None, status=status.HTTP_404_NOT_FOUND)

		serializer = LeaderboardSerializer(leaderboard, context={'request': request})
		return Response(serializer.data)
