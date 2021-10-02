# -*- coding: utf-8 -*-
"""Tests for the :mod:`biblary.views` module."""
import re

import pytest
from django.urls import reverse

from biblary.bibliography.storage import FileType


def test_biblary_index_get(get_bibliography, client):
    """Test the :class:`biblary.views:BiblaryIndexView` view ``GET`` method without storage configured."""
    with get_bibliography(bibliography_storage=None):
        url = reverse('index')
        response = client.get(url)
        content = response.content.decode(response.charset)
        assert response.status_code == 200
        assert 'Biblary' in content
        assert 'biblary-entry-files' not in content


def test_biblary_index_get_with_storage(get_bibliography, client):
    """Test the :class:`biblary.views:BiblaryIndexView` view ``GET`` method with storage configured."""
    with get_bibliography():
        url = reverse('index')
        response = client.get(url)
        content = response.content.decode(response.charset)
        assert response.status_code == 200
        assert 'Biblary' in content
        assert 'biblary-entry-files' in content


def test_biblary_file_get(get_bibliography, client):
    """Test the :class:`biblary.views:BiblaryFileView` view ``GET`` method."""
    with get_bibliography() as bibliography:
        content = b'some-content'
        file_type = FileType.MANUSCRIPT
        entry = list(bibliography.values())[0]

        url_kwargs = {
            'file_type': file_type.value,
            'identifier': entry.identifier,
        }

        bibliography.storage.put_file(content, entry, file_type)

        url = reverse('file', kwargs=url_kwargs)
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == content
        assert response.headers['Content-Type'] == 'application/pdf'
        assert response.headers['Content-Disposition'] == f'attachment; filename="{file_type.value}.pdf"'


@pytest.mark.parametrize(
    'identifier, file_type, status, match', (
        ('Einstein_1905', 'invalid', 400, r'The requested file type `.*` is invalid.'),
        ('A', 'manuscript', 404, r'The requested bibliographic entry `.*` does not exist'),
        ('Einstein_1905', 'manuscript', 404, r'The requested file `.*` does not exist.'),
    )
)
def test_biblary_file_get_raises(get_bibliography, client, identifier, file_type, status, match):
    """Test the :class:`biblary.views:BiblaryFileView` view ``GET`` method when it should raise."""
    with get_bibliography():
        kwargs = {'identifier': identifier, 'file_type': file_type}
        url = reverse('file', kwargs=kwargs)
        response = client.get(url)

        try:
            exception = response.context['exception_value']
        except KeyError:
            exception = response.context['exception']

        assert response.status_code == status
        assert re.match(match, exception)
