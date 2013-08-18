from diary.models import Post, DiaryUser
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from api.serializers import PostSerializer, PostCreateSerializer, PublicPostSerializer, ProfileSerializer
from rest_framework.response import Response
import datetime
from rest_framework import status, mixins
from django.utils.translation import ugettext_lazy as _


class ProfileDetail(mixins.UpdateModelMixin, GenericAPIView):
	model = DiaryUser
	serializer_class = ProfileSerializer

	def get(self, request, format=None):
		serializer = ProfileSerializer(request.user)
		return Response(serializer.data)

	def put(self, request, *args, **kwargs):
		kwargs["pk"] = request.user.pk
		return self.update(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		kwargs["pk"] = request.user.pk
		return self.partial_update(request, *args, **kwargs)

	def get_object(self, queryset=None):
		return self.request.user



class PostList(ListCreateAPIView):
	"""
	List your recent posts
	"""
	serializer_class=PostSerializer
	def get(self, request, format=None):
		today = datetime.date.today()
		weekago = today - datetime.timedelta(days=7)
		posts = Post.objects.filter(author=request.user, date__gte=weekago)
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		request.DATA["author"] = request.user.pk
		serializer = PostCreateSerializer(data=request.DATA, files=request.FILES)

		if serializer.is_valid():
			self.pre_save(serializer.object)
			self.object = serializer.save(force_insert=True)
			self.post_save(self.object, created=True)
			serializer = PostSerializer(self.object)
			print self.object
			print serializer
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(RetrieveUpdateDestroyAPIView):
	"""
	Show a single post
	"""
	queryset = Post.objects.all()
	serializer_class = PostSerializer


	def put(self, request, *args, **kwargs):
		today = datetime.date.today()
		object = Post.objects.get(pk=kwargs["pk"])
		if (today - object.date).days > 3:
			return Response({"Error":_("This entry is to old and can't be edited")}, status=status.HTTP_400_BAD_REQUEST)
		return uper(PostDetail, self).update(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		today = datetime.date.today()
		object = Post.objects.get(pk=kwargs["pk"])
		if (today - object.date).days > 3:
			return Response({"Error":_("This entry is to old and can't be edited")}, status=status.HTTP_400_BAD_REQUEST)
		return uper(PostDetail, self).partial_update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		today = datetime.date.today()
		object = Post.objects.get(pk=kwargs["pk"])
		if (today - object.date).days > 3:
			return Response({"Error":_("This entry is to old and can't be edited")}, status=status.HTTP_400_BAD_REQUEST)
		return  super(PostDetail, self).destroy(request, *args, **kwargs)

class PublicPostDetail(APIView):
	"""
	get a random public post
	"""
	def get(self, request, format=None):
		try:
			randompost = Post.objects.filter(author__userprofile__public = True).order_by('?')[:1].get()
			serializer = PublicPostSerializer(randompost)
			return Response(serializer.data)
		except Post.DoesNotExist:
			randompost = None