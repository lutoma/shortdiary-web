from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from diary.models import Post
from .serializers import UserSerializer, PostSerializer, PrivatePostSerializer, UserStatsSerializer


class CurrentUserView(APIView):
	def get(self, request):
		serializer = UserSerializer(request.user, context={'request': request})
		return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-date')
	serializer_class = PrivatePostSerializer


class UserStatsView(APIView):
	def get(self, request):
		serializer = UserStatsSerializer(request.user, context={'request': request})
		return Response(serializer.data)


class RandomPublicPostView(APIView):
#	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			randompost = Post.objects.filter(public=True).order_by('?').first()
			serializer = PostSerializer(randompost, context={'request': request})
			return Response(serializer.data)
		except Post.DoesNotExist:
			randompost = None
