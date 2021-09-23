# -*- coding: utf-8 -*-
"""Module that defines the views of this application."""
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from .bibliography import Bibliography
from .settings import settings


class BiblaryIndexView(TemplateView):
    """View with index of bibliography contents."""

    template_name = 'biblary/index.html'

    @staticmethod
    def get_bibliography() -> Bibliography:
        """Load the bibliography with bibliographic entries."""
        bibliography_adapter = settings.bibliography_adapter
        bibliography_adapter_configuration = settings.bibliography_adapter_configuration

        adapter_module_name, _, adapter_class_name = bibliography_adapter.rpartition('.')

        try:
            adapter_module = import_module(adapter_module_name)
        except (ImportError, ValueError) as exc:
            raise ImproperlyConfigured(
                f'module of the configured bibliography adapter `{bibliography_adapter}` cannot be imported.'
            ) from exc

        try:
            adapter_class = getattr(adapter_module, adapter_class_name)
        except AttributeError as exc:
            raise ImproperlyConfigured(
                f'class of the configured bibliography adapter `{bibliography_adapter}` cannot be imported.'
            ) from exc

        try:
            adapter = adapter_class(**bibliography_adapter_configuration)
        except Exception as exc:
            raise ImproperlyConfigured(
                'failed to construct bibliography adapter with the provided configuration:\n'
                f'{bibliography_adapter_configuration}'
            ) from exc

        return Bibliography(adapter)

    def get_context_data(self, **kwargs):
        """Add the entries of the bibliography to the context."""
        context = super().get_context_data(**kwargs)
        context['entries'] = self.get_bibliography().get_entries(sort=lambda entry: entry.year, reverse=True)
        return context
