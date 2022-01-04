# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Tests for the :mod:`biblary.bibliography.adapter.bibtex` module."""
import pytest

from biblary.bibliography.adapter.bibtex import BibtexBibliography
from biblary.bibliography.entry import BibliographyEntry
from biblary.bibliography.exceptions import BibliographicEntryParsingError


def test_get_entries(filepath_bibtex):
    """Test the :meth:`biblary.bibliography.adapter.bibtex.BibtexBibliography.get_entries` method."""
    adapter = BibtexBibliography(filepath_bibtex)
    entries = adapter.get_entries()
    assert isinstance(entries, list)
    assert len(entries) == 1
    assert isinstance(entries[0], BibliographyEntry)


def test_get_entries_excepts(tmp_path):
    """Test the :meth:`biblary.bibliography.adapter.bibtex.BibtexBibliography.get_entries` method when it excepts."""
    filepath_bibtex = tmp_path / 'bibliography.bib'
    filepath_bibtex.write_text('invalid')

    with pytest.raises(BibliographicEntryParsingError, match='failed to parse entries from bibliography.'):
        BibtexBibliography(filepath_bibtex).get_entries()


def test_parse_entry(filepath_bibtex):
    """Test the :meth:`biblary.bibliography.adapter.bibtex.BibtexBibliography.parse_entry` method."""
    entry = BibtexBibliography(filepath_bibtex).parse_entry(filepath_bibtex.read_text())
    assert isinstance(entry, BibliographyEntry)


def test_parse_entry_excepts(filepath_bibtex):
    """Test the :meth:`biblary.bibliography.adapter.bibtex.BibtexBibliography.parse_entry` method when it excepts."""
    with pytest.raises(BibliographicEntryParsingError, match='failed to parse entries from bibliography.'):
        BibtexBibliography(filepath_bibtex).parse_entry('invalid')


def test_save_entries(filepath_bibtex, get_bibliography_entry):
    """Test the :meth:`biblary.bibliography.adapter.bibtex.BibtexBibliography.save_entries` method."""
    adapter = BibtexBibliography(filepath_bibtex)
    entries = adapter.get_entries()
    entries.append(get_bibliography_entry(doi='120', identifier='Einstein', author=['TEsting']))
    adapter.save_entries(entries)

    # Construct new adapter from the same filepath to which the entries were written and retrieve entries to compare.
    adapter = BibtexBibliography(adapter.filepath)
    assert sorted(adapter.get_entries(), key=lambda e: e.identifier) == sorted(entries, key=lambda e: e.identifier)
