#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^(?P<species>\d+)\-?(?P<form>\d{1})?$', views.show_stats, name='stat'),
    path("meta/", views.display_meta, name='meta'),
    re_path("^(?P<species>\d+)\-?\d?\/(?P<loc>(next|prev))/?$", views.nearby_pkm),
]