# -*- coding: utf-8 -*-
"""Tests for the :mod:`biblary.views` module."""
import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

from biblary.bibliography import Bibliography
from biblary.views import BiblaryIndexView


def test_biblary_index_get(override_settings, client, filepath_bibtex):
    """Test the :class:`biblary.views:BiblaryIndexView` view ``GET`` method."""
    with override_settings(bibliography_adapter_configuration={'filepath': filepath_bibtex}):
        url = reverse('index')
        response = client.get(url)
        content = response.content.decode(response.charset)
        assert response.status_code == 200
        assert 'Biblary' in content


@pytest.mark.parametrize(
    'adapter, configuration, exception, match', (
        ('non.adapter.BibliographyAdapter', {}, ImproperlyConfigured, r'module of the .* cannot be imported.'),
        ('biblary.bibliography.adapter.Adapter', {}, ImproperlyConfigured, r'class of the .* cannot be imported.'),
        ('biblary.bibliography.adapter.BibtexBibliography', {}, ImproperlyConfigured, r'failed to construct.* adapter'),
    )
)
def test_biblary_index_get_bibliography_invalid_configuration(
    override_settings, adapter, configuration, exception, match
):
    """Test the :meth:`biblary.views:BiblaryIndexView.get_bibliography` method for invalid configurations."""
    with override_settings(bibliography_adapter=adapter, bibliography_adapter_configuration=configuration):
        with pytest.raises(exception, match=match):
            BiblaryIndexView().get_bibliography()


def test_biblary_index_get_bibliography(override_settings, filepath_bibtex):
    """Test the :meth:`biblary.views:BiblaryIndexView.get_bibliography` method."""
    with override_settings(bibliography_adapter_configuration={'filepath': filepath_bibtex}):
        bibliography = BiblaryIndexView().get_bibliography()
        assert isinstance(bibliography, Bibliography)
        assert bibliography.adapter.filepath == filepath_bibtex
