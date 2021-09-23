# -*- coding: utf-8 -*-
"""Module that defines the URLs of this application."""
from django.urls import path

from .views import BiblaryIndexView

app_name = 'biblary'  # pylint: disable=invalid-name

urlpatterns = [
    path('', BiblaryIndexView.as_view(), name='index'),
]
