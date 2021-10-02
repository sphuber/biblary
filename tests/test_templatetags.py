# -*- coding: utf-8 -*-
"""Tests for the :mod:`biblary.templatetags` module."""
import pytest

from biblary.templatetags.authors import main_author_class


@pytest.mark.parametrize('patterns', (('A. Einstein',), (r'.*Einstein',)))
def test_authors_main_author_class(get_bibliography, patterns):
    """Test the :class:`biblary.templatetags.authors:main_author_class` template tag."""
    with get_bibliography(bibliography_main_author_patterns=patterns):
        assert main_author_class('A. Einstein') is not None
        assert main_author_class('E. Schrödinger') is None


@pytest.mark.parametrize('patterns', (('A. Einstein'), (r'.*Einstein')))
def test_authors_main_author_class_raises(get_bibliography, patterns):
    """Test the :class:`biblary.templatetags.authors:main_author_class` template tag when it should raise."""
    with get_bibliography(bibliography_main_author_patterns=patterns):
        with pytest.raises(TypeError):
            main_author_class('A. Einstein')


def test_authors_main_author_class_custom_class(get_bibliography):
    """Test the :class:`biblary.templatetags.authors:main_author_class` template tag with custom class."""
    patterns = ('A. Einstein',)
    custom_class = 'custom-class'

    with get_bibliography(bibliography_main_author_patterns=patterns, bibliography_main_author_class=custom_class):
        assert main_author_class('A. Einstein') == custom_class
