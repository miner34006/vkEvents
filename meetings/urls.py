# -*- coding: utf-8 -*-

from django.conf.urls import url
from meetings import views

urlpatterns = [
    url(r'events/$', views.events, name='events'),
    url(r'changeEventStatus/$', views.changeEventStatus),
    url(r'relatedMembers/$', views.relatedMembers, name='relatedMembers'),
    url(r'getMemberInfo/$', views.getMemberInfo, name='getMemberInfo'),
    url(r'rateUser/$', views.rateUser, name='rateUser'),
    url(r'^$', views.initialization, name='initialization'),
]