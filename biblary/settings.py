# -*- coding: utf-8 -*-
"""Module that defines a class through which application configuration settings can be retrieved."""
import typing as t


class Settings:
    """Container to provide configuration settings for the application."""

    def __init__(self, prefix: str):
        """Initialize the class.

        :param prefix: the prefix with which application settings can be configured globally. The prefix will be
            automatically converted to all uppercase.
        """
        self.prefix = prefix.upper()

    def _get_setting(self, name: str, default: t.Any) -> t.Any:
        """Retrieve the setting with the given name from the loaded settings or return the specified default.

        .. note:: The module :mod:`django.conf.settings` needs to be imported in this method for it to be up to date.
        """
        from django.conf import settings as django_settings
        return getattr(django_settings, f'{self.prefix}_{name}', default)

    @property
    def bibliography_adapter(self) -> str:
        """Return the full import path of the bibliography adapter implementation to use.

        The value should be an implementation of :class:`biblary.bibliography.adapter.abstract.BibliographyAdapter`.
        """
        return self._get_setting('BIBLIOGRAPHY_ADAPTER', 'biblary.bibliography.adapter.bibtex.BibtexBibliography')

    @property
    def bibliography_adapter_configuration(self) -> dict:
        """Return the dictionary that will be passed as keyword arguments of the bibliography adapter constructor."""
        return self._get_setting('BIBLIOGRAPHY_ADAPTER_CONFIGURATION', {})


settings: Settings = Settings('BIBLARY')
