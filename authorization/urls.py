# -*- coding: utf-8 -*-

from django.conf.urls import url
from authorization import views

urlpatterns = [
    url(r'redirect/$', views.authRedirect, name='redirect'),
    url(r'$', views.authorization, name='authorization'),
]