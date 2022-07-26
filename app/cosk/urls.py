"""cosk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from allauth.account.views import confirm_email
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import serializers, viewsets, routers




# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    path('admin/', admin.site.urls),

    re_path(r'^rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^account/', include('allauth.urls')),
    re_path(r'^account/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^account/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    #path('users/', include('users.urls')),

    #path('registration/', include('dj_rest_auth.registration.urls')),
    #path('rest-auth/', include('dj_rest_auth.urls')),
]
