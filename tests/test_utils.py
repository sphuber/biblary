# -*- coding: utf-8 -*-
"""Tests for the :mod:`biblary.utils` module."""
import pytest
from django.core.exceptions import ImproperlyConfigured

from biblary.bibliography import Bibliography
from biblary.bibliography.storage.file_system import FileSystemStorage
from biblary.utils import BibliographyMixin


def test_bibliography_mixin_construct_class(tmp_path):
    """Test the :meth:`biblary.utils.BibliographyMixin.construct_class` method."""
    classifier = 'biblary.bibliography.storage.file_system.FileSystemStorage'
    kwargs = {'filepath': tmp_path}
    instance = BibliographyMixin.construct_class(classifier, kwargs)
    assert isinstance(instance, FileSystemStorage)


def test_bibliography_mixin_construct_class_none():
    """Test the :meth:`biblary.utils.BibliographyMixin.construct_class` method when ``classifier`` is ``None``."""
    assert BibliographyMixin.construct_class(None) is None


@pytest.mark.parametrize(
    'classifier, kwargs, match', (
        ('biblary.bibliography.non_existing.FileSystemStorage', None, r'module of `.*` cannot be imported.'),
        ('biblary.bibliography.storage.file_system.NonExistingStorage', None, r'class of `.*` cannot be imported.'),
        ('biblary.bibliography.storage.file_system.FileSystemStorage', None, r'failed to construct `.*`.'),
    )
)
def test_bibliography_mixin_construct_class_raises(classifier, kwargs, match):
    """Test the :meth:`biblary.utils.BibliographyMixin.construct_class` method when it should raise."""
    with pytest.raises(ImproperlyConfigured, match=match):
        BibliographyMixin.construct_class(classifier, kwargs)


@pytest.mark.parametrize(
    'adapter, configuration, exception, match', (
        ('non.adapter.BibliographyAdapter', {}, ImproperlyConfigured, r'failed to construct the configured .*'),
        ('biblary.bibliography.adapter.Adapter', {}, ImproperlyConfigured, r'failed to construct the configured .*.'),
        ('biblary.bibliography.adapter.BibtexBibliography', {}, ImproperlyConfigured, r'failed to construct.* adapter'),
    )
)
def test_bibliography_mixin_get_bibliography_invalid_configuration(
    override_settings, adapter, configuration, exception, match
):
    """Test the :meth:`biblary.views:BiblaryIndexView.get_bibliography` method for invalid configurations."""
    with override_settings(bibliography_adapter=adapter, bibliography_adapter_configuration=configuration):
        with pytest.raises(exception, match=match):
            BibliographyMixin.get_bibliography()


def test_bibliography_mixin_get_bibliography(override_settings, filepath_bibtex):
    """Test the :meth:`biblary.views:BiblaryIndexView.get_bibliography` method."""
    with override_settings(bibliography_adapter_configuration={'filepath': filepath_bibtex}):
        bibliography = BibliographyMixin.get_bibliography()
        assert isinstance(bibliography, Bibliography)
        assert bibliography.adapter.filepath == filepath_bibtex


@pytest.mark.parametrize('storage_required', (True, False))
def test_bibliography_mixin_get_bibliography_storage_required(override_settings, filepath_bibtex, storage_required):
    """Test the ``storage_require`` argument of the :meth:`biblary.views:BiblaryIndexView.get_bibliography` method."""
    with override_settings(
        bibliography_adapter='biblary.bibliography.adapter.BibtexBibliography',
        bibliography_adapter_configuration={'filepath': filepath_bibtex}
    ):
        if storage_required:
            with pytest.raises(ImproperlyConfigured):
                BibliographyMixin.get_bibliography(storage_required=storage_required)
        else:
            bibliography = BibliographyMixin.get_bibliography(storage_required=storage_required)
            assert bibliography.storage is None
