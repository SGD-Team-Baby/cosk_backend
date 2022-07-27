from django.urls import path, include, re_path
from allauth.account.views import confirm_email

from dj_rest_auth.views import (LoginView, PasswordChangeView)
from .views import UserDetailsView, UserInfoView, UserUpdateView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('login', LoginView.as_view(), name='rest_login'),
    path('registration', include('dj_rest_auth.registration.urls')),
    re_path(r'^registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),

    path('users/<pk>', UserInfoView.as_view()),

    # URLs that require a user to be logged in with a valid session / token.
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('user/update', UserUpdateView.as_view()),
    path('password/change', PasswordChangeView.as_view(), name='rest_password_change'),

]