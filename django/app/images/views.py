import os, uuid
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from posts.models import Post
from .models import Image

# Create your views here.

FILE_COUNT_LIMIT = 1
FILE_SIZE_LIMIT = 26214400 #25M
WHITE_LIST_EXT = [
	'.jpg',
	'.jpeg',
	'.png'
]

class ImageUploadView(GenericAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user

		if len(self.request.FILES) == 0 or len(self.request.FILES) > FILE_COUNT_LIMIT:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		file = self.request.FILES['file']
		if file.content_type != 'image/jpeg' and file.content_type != 'image/png':
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if file.size > FILE_SIZE_LIMIT:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		filename, file_ext = os.path.splitext(file.name)
		if file_ext.lower() not in WHITE_LIST_EXT:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		newName = str(uuid.uuid4())
		filename = newName + file_ext

		if "post" in self.request.data:
			postId = self.request.data["post"]
			postObject = get_object_or_404(Post, id=postId)
			if post.user_id != user.id:
				return Response(status=status.HTTP_401_UNAUTHORIZED)

			path = "/upload/" + str(post.id) + "/"
		else:
			path = "/upload/tmp/"
			postObject = None

		os.makedirs(path, exist_ok=True)
		destination = open(path + filename, "wb+")
		for chunk in file.chunks():
			destination.write(chunk)
		destination.close()

		url = self.request.build_absolute_uri('/') + "image/view/" + str(filename)
		Image.objects.create(post=postObject, url=url, filename=filename)

		
		return Response(url, status=status.HTTP_201_CREATED)


class ImageView(GenericAPIView):
	permission_classes = (AllowAny, )

	def get(self, request, filename, *args, **kwargs):
		image = get_object_or_404(Image, filename=filename)
		if image.post != None:
			path = "/upload/" + str(image.post_id) + "/" + filename
		else:
			path = "/upload/tmp/" + filename

		filename, file_ext = os.path.splitext(filename)
		if file_ext == ".png":
			content_type = "image/png"
		elif file_ext == ".jpg" or file_ext == ".jpeg":
			content_type = "image/jpeg"

		with open(path, mode='rb') as file:
			return HttpResponse(file.read(), content_type=content_type)

		return Response(status=status.HTTP_404_NOT_FOUND)