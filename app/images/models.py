from django.db import models

from posts.models import Post

# Create your models here.

class Image(models.Model):
	id = models.AutoField(primary_key=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	path = models.CharField(max_length=150, blank=False)

	def __str__(self):
		return self.path