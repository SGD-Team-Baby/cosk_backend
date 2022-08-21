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
from posts.models import Post, Content, Comment, PostTag, FavoriteLog

from .serializers import PostListSerializer, PostSerializer, PostCreateSerializer, PostUpdateSerializer, CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer


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
		
		searchType = self.request.GET.get("type", "1")
		searchQuery = self.request.GET.get("query", "").strip()

		if searchQuery != "":
			if searchType == "1":
				queryset = self.searchTag(queryset, searchQuery)
			elif searchType == "2":
				queryset = self.searchTitle(queryset, searchQuery)

		data = {}
		data["total"] = queryset.count
		data["data"] = queryset[idx:idx + 20]

		serializer = self.serializer_class(data)
		return Response(serializer.data)

	def get_queryset(self):
		return Post.objects.filter(parent__isnull=True)

	def searchTag(self, queryset, tag):
		tagList = PostTag.objects.filter(tag__name__icontains=tag).values("post")
		return queryset.filter(id__in=tagList)

	def searchTitle(self, queryset, title):
		return queryset.filter(title__icontains=title)


class PostInfoView(RetrieveAPIView):
	serializer_class = PostSerializer
	permission_classes = (AllowAny, )

	def get_queryset(self):
		return Post.objects.all()

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.visit = instance.visit + 1
		instance.save()
		serializer = self.get_serializer(instance)
		return Response(serializer.data)


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



class CommentCreateView(GenericAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		postId = self.request.data["post"]

		post = get_object_or_404(Post, id=postId)

		request.data["user"] = user.id
		request.data["post"] = post.id

		serializer = CommentCreateSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			comment = serializer.save()
			return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentUpdateView(GenericAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		commentId = self.request.data["id"]

		comment = get_object_or_404(Comment, id=commentId)
		if comment.user_id != user.id:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		serializer = CommentUpdateSerializer(comment, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(GenericAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		commentId = self.request.data["id"]

		comment = get_object_or_404(Comment, id=commentId)
		if comment.user_id != user.id:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		comment.delete()
		return Response(status=status.HTTP_200_OK)


class FavoritToggleView(GenericAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		postId = request.data["post"]

		post = get_object_or_404(Post, id=postId)

		try:
			favorite = FavoriteLog.objects.get(post=post, user=user)
			favorite.delete()
			post.favorite = post.favorite - 1
			if post.favorite < 0:
				post.favorite = 0
			post.save()

			return Response(status=status.HTTP_205_RESET_CONTENT)

		except FavoriteLog.DoesNotExist:
			FavoriteLog.objects.create(post=post, user=user)
			post.favorite = post.favorite + 1
			post.save()

			return Response(status=status.HTTP_200_OK)

		return Response(status=status.HTTP_400_BAD_REQUEST)