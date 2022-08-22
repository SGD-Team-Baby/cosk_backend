from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from users.models import User

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'answer', 'question']


class UserInfoSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'name', 'answer', 'question']


class UserUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['name']




class RegisterSerializer(RegisterSerializer):
  name = serializers.CharField(required=True, max_length=150)

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data["name"] = self.validated_data.get("name", "")

    return data