# -*- coding: utf-8 -*-
"""Tests for the :mod:`biblary.views` module."""
from django.urls import reverse


def test_index(client):
    """Test the :class:`biblary.views:BiblaryIndexView` view."""
    url = reverse('index')
    response = client.get(url)
    content = response.content.decode(response.charset)
    assert response.status_code == 200
    assert 'Biblary' in content
