# -*- coding: utf-8 -*-
"""Module that defines the views of this application."""
import typing as t
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured

from .bibliography import Bibliography


class BibliographyMixin:
    """Mixin to construct the :class:`biblary.bibliography.bibliography.Bibliography` from configured settings."""

    @staticmethod
    def construct_class(classifier: t.Optional[str] = None, kwargs: t.Dict = None) -> t.Optional[t.Any]:
        """Construct instance of the class specified by the given classifier using the provided keyword arguments.

        :param classifier: fully-qualified classifier of the class to construct.
        :param kwargs: keyword arguments that are passed to the constructor of the class.
        :returns: the class instance if successfully imported and constructed.
        :raises :class`django.core.exceptions.ImproperlyConfigured`: if the module or class of the classifier cannot be
            imported, or if the construction of the loaded class fails for the provided keyword arguments.
        """
        if classifier is None:
            return None

        module_name, _, class_name = classifier.rpartition('.')

        try:
            module = import_module(module_name)
        except (ImportError, ValueError) as exc:
            raise ImproperlyConfigured(f'module of `{classifier}` cannot be imported.') from exc

        try:
            cls = getattr(module, class_name)
        except AttributeError as exc:
            raise ImproperlyConfigured(f'class of `{classifier}` cannot be imported.') from exc

        try:
            instance = cls(**kwargs or {})
        except Exception as exc:
            raise ImproperlyConfigured(f'failed to construct `{classifier}` with keyword arguments: {kwargs}') from exc

        return instance

    @classmethod
    def get_bibliography(cls) -> Bibliography:
        """Construct the bibliography with bibliographic entries from the configured settings.

        :raises :class`django.core.exceptions.ImproperlyConfigured`: if bibliography cannot be properly instantiated.
        """
        from biblary.settings import settings

        try:
            adapter = cls.construct_class(settings.bibliography_adapter, settings.bibliography_adapter_configuration)
        except ImproperlyConfigured as exc:
            raise ImproperlyConfigured(f'failed to construct the configured bibliography adapter: {exc}') from exc

        if adapter is None:
            raise ImproperlyConfigured('no bibliography adapter has been configured.')

        try:
            storage = cls.construct_class(settings.bibliography_storage, settings.bibliography_storage_configuration)
        except ImproperlyConfigured as exc:
            raise ImproperlyConfigured(f'failed to construct the configured bibliography storage: {exc}') from exc

        return Bibliography(adapter, storage=storage)
