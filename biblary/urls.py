# -*- coding: utf-8 -*-
"""Module that defines the URLs of this application."""
from django.urls import path

from .views import BiblaryFileView, BiblaryIndexView, BiblaryUploadEntryView, BiblaryUploadFileView

app_name = 'biblary'  # pylint: disable=invalid-name

urlpatterns = [
    path('', BiblaryIndexView.as_view(), name='index'),
    path('upload-entry', BiblaryUploadEntryView.as_view(), name='upload-entry'),
    path('upload-file', BiblaryUploadFileView.as_view(), name='upload-file'),
    path('file/<identifier>/<file_type>', BiblaryFileView.as_view(), name='file'),
]
