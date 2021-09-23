# -*- coding: utf-8 -*-
"""Tests for the :mod:`biblary.bibliography.entry` module."""
import pytest

from biblary.bibliography.entry import BibliographyEntry


def test_bibliography_entry_constructor():
    """Test the class:`biblary.bibliography.entry.BibliographyEntry` constructor with minimal arguments."""
    entry_type = 'article'
    identifier = 'Einstein1905'
    entry = BibliographyEntry(entry_type=entry_type, identifier=identifier)
    assert entry.entry_type == entry_type
    assert entry.identifier == identifier


def test_bibliography_entry_constructor_invalid():
    """Test the class:`biblary.bibliography.entry.BibliographyEntry` constructor with insufficient arguments."""
    with pytest.raises(TypeError, match=r'missing .* required positional arguments'):
        BibliographyEntry()  # pylint: disable=no-value-for-parameter
