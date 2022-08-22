from django.urls import path, include, re_path
from allauth.account.views import confirm_email

from .views import PostListView, PostInfoView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView, FavoritToggleView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('list', PostListView.as_view()),
    path('info/<pk>', PostInfoView.as_view()),

    
    # URLs that require a user to be logged in with a valid session / token.
    path('create', PostCreateView.as_view()),
    path('update', PostUpdateView.as_view()),
    path('delete', PostDeleteView.as_view()),

    path('comment/create', CommentCreateView.as_view()),
    path('comment/update', CommentUpdateView.as_view()),
    path('comment/delete', CommentDeleteView.as_view()),

    path('favorite', FavoritToggleView.as_view()),

]