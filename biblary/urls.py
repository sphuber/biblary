# -*- coding: utf-8 -*-
"""Module that defines the URLs of this application."""
from django.urls import path

from .views import BiblaryFileView, BiblaryIndexView

app_name = 'biblary'  # pylint: disable=invalid-name

urlpatterns = [
    path('', BiblaryIndexView.as_view(), name='index'),
    path('file/<identifier>/<file_type>', BiblaryFileView.as_view(), name='file'),
]
