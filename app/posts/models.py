from django.db import models

from users.models import User
from tags.models import Tag

from .validators import validateContentType

# Create your models here.

class Post(models.Model):
	id = models.AutoField(primary_key=True)
	parent = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	title = models.CharField(max_length=150)
	favorite = models.IntegerField(default=0)
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Content(models.Model):
	id = models.AutoField(primary_key=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	type = models.CharField(max_length=10, validators=[validateContentType])
	text = models.TextField()

	def __str__(self):
		return self.type

class PostTag(models.Model):
	id = models.AutoField(primary_key=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

	def __str__(self):
		return self.tag_id