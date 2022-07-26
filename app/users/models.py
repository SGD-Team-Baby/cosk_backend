from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
  username = None
  email = models.EmailField('email address', unique=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()

  name = models.CharField(max_length=150, unique=True)
  answer = models.IntegerField(default=0)
  question = models.IntegerField(default=0)


  def __str__(self):
    return self.email