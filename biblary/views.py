# -*- coding: utf-8 -*-
"""Module that defines the views of this application."""
from django.views.generic import TemplateView


class BiblaryIndexView(TemplateView):
    """View with index of bibliography contents."""

    template_name = 'biblary/index.html'
