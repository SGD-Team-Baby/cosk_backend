from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from allauth.account.utils import send_email_confirmation

from .models import User
from allauth.account.models import EmailAddress

from .serializers import UserSerializer, UserInfoSerializer, UserUpdateSerializer

class UserDetailsView(RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated, )

	def get_object(self):
		return self.request.user

	def get_queryset(self):
		return get_user_model().objects.none()


class UserInfoView(RetrieveAPIView):
	serializer_class = UserInfoSerializer
	permission_classes = (AllowAny, )

	def get_queryset(self):
		return User.objects.all()


class UserUpdateView(GenericAPIView):
	serializer_class = UserUpdateSerializer
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		serializer = UserUpdateSerializer(user, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailResendView(GenericAPIView):
	permission_classes = (AllowAny, )

	def post(self, request, *args, **kwargs):
		email_address = self._get_email_address(request)
		if email_address:
			send_email_confirmation(
				self.request, email_address.user, email=email_address.email
			)

		getter = getattr(
			settings,
			"ALLAUTH_SETTING_GETTER",
			lambda name, dflt: getattr(settings, name, dflt),
		)
		url = getter("ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL", None)		
		return redirect(url)

	def _get_email_address(self, request):
		email = request.POST["email"]
		try:
			return EmailAddress.objects.get(email=email)
		except EmailAddress.DoesNotExist:
			pass

	