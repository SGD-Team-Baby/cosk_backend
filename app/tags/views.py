import os, shutil
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Tag
from posts.models import Post, Content, PostTag

from .serializers import TagSerializer, TagCountSerializer

class TagListView(GenericAPIView):
  permission_classes = (AllowAny, )

  def get(self, request, *args, **kwargs):
    queryset = Tag.objects.annotate(count=Count('posttag__tag')).order_by('-count')
    queryset = queryset[:10]
    
    return Response(TagCountSerializer(queryset, many=True).data)

class TagSearchView(GenericAPIView):
  permission_classes = (AllowAny, )

  def get(self, request, query, *args, **kwargs):
    searchQuery = query.strip()
    queryset = Tag.objects.filter(name__icontains=searchQuery)[:5]
    
    return Response(TagSerializer(queryset, many=True).data)
