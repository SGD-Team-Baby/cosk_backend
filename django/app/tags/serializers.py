from rest_framework import serializers

from .models import Tag
from posts.models import Post, Content, PostTag

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = ['name']


class TagCountSerializer(serializers.ModelSerializer):
	count = serializers.SerializerMethodField()

	class Meta:
		model = Tag
		fields = ['name', 'count']

	def get_count(self, obj):
		return PostTag.objects.filter(tag=obj.id).count()