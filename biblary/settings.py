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

    @property
    def bibliography_storage(self) -> t.Optional[str]:
        """Return the full import path of the bibliography storage implementation to use.

        The value should be an implementation of :class:`biblary.bibliography.storage.abstract.AbstractStorage`.
        """
        return self._get_setting('BIBLIOGRAPHY_STORAGE', None)

    @property
    def bibliography_storage_configuration(self) -> dict:
        """Return the dictionary that will be passed as keyword arguments of the bibliography storage constructor."""
        return self._get_setting('BIBLIOGRAPHY_STORAGE_CONFIGURATION', {})

    @property
    def bibliography_main_author_patterns(self) -> t.Sequence[str]:
        """Return a sequence of strings that represent authors that should be marked as main author.

        The elements of the sequence can be simple strings or regex patterns.
        """
        return self._get_setting('BIBLIOGRAPHY_MAIN_AUTHOR_PATTERNS', ())

    @property
    def bibliography_main_author_class(self) -> str:
        """Return the CSS class that is used by the :meth:`biblary.templatetags.authors.main_author_class`.

        This tag can be used in the index template to add this CSS class to main authors.
        """
        return self._get_setting('BIBLIOGRAPHY_MAIN_AUTHOR_CLASS', 'biblary-entry-author-main')


settings: Settings = Settings('BIBLARY')
