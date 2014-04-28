from diary.models import Post, DiaryUser
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from api.serializers import PostSerializer, PostCreateSerializer, PublicPostSerializer, ProfileSerializer
from rest_framework.response import Response
import datetime
from rest_framework import status, mixins
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import AllowAny


class ProfileDetail(mixins.UpdateModelMixin, GenericAPIView):
	model = DiaryUser
	serializer_class = ProfileSerializer

	def get(self, request, format=None):
		serializer = self.serializer_class(request.user)
		return Response(serializer.data)

	def put(self, request, *args, **kwargs):
		kwargs["pk"] = request.user.pk
		if request.DATA["email"] != request.user.email:
			request.user.mail_verified = False
			request.user.save()
		response = self.update(request, *args, **kwargs)
		if request.user.mail_verified == False:
			request.user.send_verification_mail()
		return response

	def patch(self, request, *args, **kwargs):
		kwargs["pk"] = request.user.pk
		if request.DATA["email"] != request.user.email:
			request.user.mail_verified = False
			request.user.save()
		response = self.partial_update(request, *args, **kwargs)
		if request.user.mail_verified == False:
			request.user.send_verification_mail()
		return response

	def get_object(self, queryset=None):
		return self.request.user



class PostList(ListCreateAPIView):
	"""
	List your posts
	"""
	serializer_class=PostSerializer
	def get(self, request, format=None):
		posts = Post.objects.filter(author=request.user).order_by("-date")
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		data = request.DATA.copy()
		data["author"] = request.user.pk
		serializer = PostCreateSerializer(data=data, files=request.FILES)

		if serializer.is_valid():
			self.pre_save(serializer.object)
			self.object = serializer.save(force_insert=True)
			self.post_save(self.object, created=True)
			serializer = PostSerializer(self.object)
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

	def get(self, request, *args, **kwargs):
		object = Post.objects.get(pk=kwargs["pk"])
		return super(PostDetail, self).get(request, *args, **kwargs)


	def put(self, request, *args, **kwargs):
		today = datetime.date.today()
		object = Post.objects.get(pk=kwargs["pk"])
		if (today - object.date).days > 3:
			return Response({"Error":_("This entry is too old and can't be edited")}, status=status.HTTP_400_BAD_REQUEST)
		return super(PostDetail, self).update(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		today = datetime.date.today()
		object = Post.objects.get(pk=kwargs["pk"])
		if (today - object.date).days > 3:
			return Response({"Error":_("This entry is too old and can't be edited")}, status=status.HTTP_400_BAD_REQUEST)
		return super(PostDetail, self).partial_update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		today = datetime.date.today()
		object = Post.objects.get(pk=kwargs["pk"])
		if (today - object.date).days > 3:
			return Response({"Error":_("This entry is to old and can't be edited")}, status=status.HTTP_400_BAD_REQUEST)
		return  super(PostDetail, self).destroy(request, *args, **kwargs)

class PostYearAgo(GenericAPIView):
	serializer_class = PostSerializer

	def get(self, request, format=None):
		today = datetime.date.today()
		yearago = datetime.date(today.year-1, today.month, today.day)
		try:
			post = Post.objects.get(author=request.user, date=yearago)
			serializer = self.serializer_class(post)
			response = Response(serializer.data)
		except:
			response = Response({"No post for last year"})
			response.status_code = 404
		return response


class PublicPostDetail(APIView):
	"""
	get a random public post
	"""

	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			randompost = Post.objects.filter(public = True).order_by('?')[:1].get()
			serializer = PublicPostSerializer(randompost)
			return Response(serializer.data)
		except Post.DoesNotExist:
			randompost = None