import os, shutil
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from posts.models import Post, Content, PostTag

from .serializers import PostListSerializer, PostSerializer, PostCreateSerializer, PostUpdateSerializer


class PostListView(GenericAPIView):
	serializer_class = PostListSerializer
	permission_classes = (AllowAny, )

	def get(self, request, *args, **kwargs):
		pageNum = self.request.GET.get("page", "1")
		if not pageNum.isnumeric() or int(pageNum) <= 0:
			pageNum = 1
		else:
			pageNum = int(pageNum)
		
		idx = 20 * (pageNum - 1)

		queryset = self.get_queryset()

		data = {}
		data["total"] = queryset.count
		data["data"] = queryset[idx:idx + 20]

		serializer = self.serializer_class(data)
		return Response(serializer.data)

	def get_queryset(self):
		return Post.objects.filter(parent__isnull=True)


class PostInfoView(RetrieveAPIView):
	serializer_class = PostSerializer
	permission_classes = (AllowAny, )

	def get_queryset(self):
		return Post.objects.all()



class PostCreateView(GenericAPIView):
	serializer_class = PostCreateSerializer
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		request.data["user"] = user.id

		parentId = request.data["parent"]
		if parentId != None:
			post = get_object_or_404(Post, id=parentId)
			if post.parent_id != None:
				return Response(status=status.HTTP_400_BAD_REQUEST)

		serializer = PostCreateSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			post = serializer.save()
			return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostUpdateView(GenericAPIView):
	serializer_class = PostUpdateSerializer
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		postId = self.request.data["id"]

		post = get_object_or_404(Post, id=postId)
		if post.user_id != user.id:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		serializer = PostUpdateSerializer(post, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteView(GenericAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		postId = self.request.data["id"]

		post = get_object_or_404(Post, id=postId)
		if post.user_id != user.id:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		upload_path = "/upload/" + str(post.id)
		if os.path.exists(upload_path):
			shutil.rmtree(upload_path)

		post.delete()
		return Response(status=status.HTTP_200_OK)

