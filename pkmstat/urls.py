#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^(?P<species>\d+)\-?(?P<form>\d{1})?$', views.show_stats, name='stat'),
    path("meta/", views.display_meta, name='meta'),
    path("next/", views.nearby_pkm, name='next', kwargs={'loc': 'next'}),
    path("prev/", views.nearby_pkm, name='prev', kwargs={'loc': 'prev'}),
]