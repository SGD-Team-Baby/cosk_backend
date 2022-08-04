from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from users.models import User
from posts.models import Post, Content, PostTag

from users.serializers import UserSerializer, UserInfoSerializer



class ContentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Content
		fields = ['type', 'text']


class PostRootSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer(read_only=True)
	contents = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ['id', 'user', 'title', 'contents', 'favorite', 'time']

	def get_contents(self, obj):
		contents = Content.objects.filter(post=obj.id)
		return ContentSerializer(contents, many=True, read_only=True).data


class PostListSerializer(serializers.Serializer):
	data = PostRootSerializer(many=True, read_only=True)
	total = serializers.IntegerField(default=0)

	def create(self, validated_data):
		return {data, total}

	def get_total(self, obj):
		contents = Content.objects.filter(post=obj.id)
		return ContentSerializer(contents, many=True, read_only=True).data


class PostSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer(read_only=True)
	contents = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ['id', 'user', 'title', 'contents', 'comments', 'favorite', 'time']

	def get_contents(self, obj):
		contents = Content.objects.filter(post=obj.id)
		return ContentSerializer(contents, many=True, read_only=True).data

	def get_comments(self, obj):
		post = Post.objects.filter(parent=obj.id)
		return PostSerializer(post, many=True, read_only=True).data





class PostCreateSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)

	class Meta:
		model = Post
		fields = ['parent', 'user', 'title', 'contents']


	def create(self, validated_data):
		contents = validated_data.pop("contents")
		post = Post.objects.create(**validated_data)
		for content in contents:
			Content.objects.create(post=post, **content)
		return post


class PostUpdateSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)

	class Meta:
		model = Post
		fields = ['id', 'title', 'contents']


	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.save()

		delete = Content.objects.filter(post=instance.id)
		delete.delete()

		contents = validated_data.pop("contents")
		for content in contents:
			Content.objects.create(post=instance, **content)
		return instance