from django.urls import path, include, re_path
from allauth.account.views import confirm_email

from .views import ImageView, ImageUploadView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('view/<filename>', ImageView.as_view()),
    
    # URLs that require a user to be logged in with a valid session / token.
    path('upload', ImageUploadView.as_view()),

]