from rest_framework import serializers

from users.models import User
from tags.models import Tag
from posts.models import Post, Content, PostTag

from users.serializers import UserSerializer, UserInfoSerializer
from tags.serializers import TagSerializer


class ContentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Content
		fields = ['type', 'text', 'options']


class PostRootSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer(read_only=True)
	contents = serializers.SerializerMethodField()
	tags = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ['id', 'user', 'title', 'contents', 'favorite', 'time', 'tags']

	def get_contents(self, obj):
		contents = Content.objects.filter(post=obj.id)
		return ContentSerializer(contents, many=True, read_only=True).data

	def get_tags(self, obj):
		postTag = PostTag.objects.filter(post=obj.id).values('tag__name')
		tags = []
		for tag in postTag:
			tags.append(tag["tag__name"])

		return tags


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
	tags = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ['id', 'user', 'title', 'contents', 'comments', 'favorite', 'time', 'tags']

	def get_contents(self, obj):
		contents = Content.objects.filter(post=obj.id)
		return ContentSerializer(contents, many=True, read_only=True).data

	def get_comments(self, obj):
		post = Post.objects.filter(parent=obj.id)
		return PostSerializer(post, many=True, read_only=True).data

	def get_tags(self, obj):
		postTag = PostTag.objects.filter(post=obj.id).values('tag__name')
		tags = []
		for tag in postTag:
			tags.append(tag["tag__name"])

		return tags


class PostCreateSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)
	tags = serializers.ListField(child=serializers.CharField(max_length=100))

	class Meta:
		model = Post
		fields = ['parent', 'user', 'title', 'contents', 'tags']


	def create(self, validated_data):
		contents = validated_data.pop("contents")
		tags = validated_data.pop("tags")
		post = Post.objects.create(**validated_data)

		for content in contents:
			Content.objects.create(post=post, **content)

		for tagName in tags:
			tag, created = Tag.objects.get_or_create(name=tagName)
			PostTag.objects.create(post=post, tag=tag)

		return post


class PostUpdateSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)
	tags = serializers.ListField(child=serializers.CharField(max_length=100))

	class Meta:
		model = Post
		fields = ['id', 'title', 'contents', 'tags']


	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.save()

		contentBefore = Content.objects.filter(post=instance.id)
		contentBefore.delete()

		tagBefore = PostTag.objects.filter(post=instance.id)
		tagBefore.delete()

		contents = validated_data.pop("contents")
		for content in contents:
			Content.objects.create(post=instance, **content)

		tags = validated_data.pop("tags")
		for tagName in tags:
			tag, created = Tag.objects.get_or_create(name=tagName)
			PostTag.objects.create(post=instance, tag=tag)

		return instance
