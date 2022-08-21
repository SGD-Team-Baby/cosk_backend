from django.urls import path, include, re_path
from allauth.account.views import confirm_email

from .views import TagListView, TagSearchView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('list', TagListView.as_view()),
    path('search/<query>', TagSearchView.as_view()),
    
    # URLs that require a user to be logged in with a valid session / token.

]