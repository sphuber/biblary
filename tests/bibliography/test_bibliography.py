# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Tests for the :mod:`biblary.bibliography.bibliography` module."""
import io
import json
import typing as t

import pytest

from biblary.bibliography.adapter import BibliographyAdapter, BibtexBibliography
from biblary.bibliography.bibliography import Bibliography
from biblary.bibliography.entry import BibliographyEntry
from biblary.bibliography.exceptions import (
    BibliographicEntryParsingError,
    DuplicateEntryError,
    InvalidBibliographyError,
)
from biblary.bibliography.storage import AbstractStorage, FileType


class MockAdapter(BibliographyAdapter):
    """Mock implementation of :class:`biblary.bibliography.adapter.abstract.BibliographyAdapter`."""

    def __init__(self, *args, entries=None, **kwargs):
        """Construct new instance for a list of entries."""
        super().__init__(*args, **kwargs)
        self._entries = entries

    def get_entries(self):
        """Return the list of bibliographic entries for this bibliography."""
        return self._entries

    @classmethod
    def parse_entry(cls, content: str) -> BibliographyEntry:
        """Parse a new bibliographic entry from a string."""
        try:
            return BibliographyEntry(**json.loads(content))
        except json.JSONDecodeError as exception:
            raise BibliographicEntryParsingError() from exception

    @classmethod
    def write_entry(cls, entry, stream) -> None:
        """Write a bibliographic entry formatted as text to the given stream."""

    def save_entries(self, entries: t.List[BibliographyEntry]) -> None:
        """Save the list of entries to the bibliography."""


class MockStorage(AbstractStorage):
    """Mock implementation of :class:`biblary.bibliography.adapter.abstract.BibliographyAdapter`."""

    def get_file(self, entry: BibliographyEntry, file_type: t.Union[FileType, str]) -> bytes:
        """Return the byte content of a file with the given type for the given bibliographic entry."""
        return b''

    def put_file(self, content: t.Union[io.BytesIO, bytes], entry: BibliographyEntry, file_type: FileType) -> None:
        """Write the given byte content for the given bibliographic entry and file type."""

    def exists(self, entry: BibliographyEntry, file_type: t.Union[FileType, str]) -> bool:
        """Return whether the file with the given type for the given bibliographic entry exists."""
        return True


@pytest.fixture
def get_bibliography() -> Bibliography:
    """Return an instance of a :class:`biblary.bibliography.adapter.abstract.BibliographyAdapter`."""

    def _fixture(entries=None) -> t.Callable:
        if entries is None:
            entries = [
                BibliographyEntry('article', identifier=1, year=1901, author='M. Planck'),
                BibliographyEntry('article', identifier=2, year=1905, author='A. Einstein'),
                BibliographyEntry('article', identifier=3, year=1913, author='N. Bohr'),
                BibliographyEntry('article', identifier=4, year=1916, author='A. Einstein'),
            ]
        adapter = MockAdapter(entries=entries)
        return Bibliography(adapter=adapter)

    return _fixture


def test_bibliography_constructor():
    """Test the :class:`biblary.bibliography.bibliography.Bibliography` constructor with minimal arguments."""
    adapter = MockAdapter()
    bibliography = Bibliography(adapter=adapter)
    assert bibliography.adapter is adapter

    storage = MockStorage()
    bibliography = Bibliography(adapter=adapter, storage=storage)
    assert bibliography.storage is storage


def test_bibliography_constructor_invalid():
    """Test the :class:`biblary.bibliography.bibliography.Bibliography` constructor with incorrect arguments."""
    with pytest.raises(TypeError, match='`adapter` should be an instance of `BibliographyAdapter`'):
        Bibliography(adapter='invalid-type')

    with pytest.raises(InvalidBibliographyError, match='bibliography contains entries with duplicate identifiers'):
        entries = [BibliographyEntry('a', identifier=1), BibliographyEntry('a', identifier=1)]
        adapter = MockAdapter(entries=entries)
        Bibliography(adapter=adapter)


@pytest.mark.parametrize('entries', (([]), ([BibliographyEntry('a', 1), BibliographyEntry('a', 2)])))
def test_get_item(get_bibliography, entries):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__getitem__` method."""
    bibliography = get_bibliography(entries)

    for entry in entries:
        assert bibliography[entry.identifier] is entry


@pytest.mark.parametrize('entries', (([]), ([BibliographyEntry('a', 1), BibliographyEntry('a', 2)])))
def test_iter(get_bibliography, entries):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__iter__` method."""
    bibliography = get_bibliography(entries)

    for identifier in bibliography:
        assert isinstance(bibliography[identifier], BibliographyEntry)


@pytest.mark.parametrize('entries', (([]), ([BibliographyEntry('a', 1), BibliographyEntry('a', 2)])))
def test_len(get_bibliography, entries):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__len__` method."""
    bibliography = get_bibliography(entries)
    assert len(bibliography) == len(entries)


def test_contains(get_bibliography, get_bibliography_entry):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__contains__` method."""
    entry_one = get_bibliography_entry()
    entry_two = get_bibliography_entry()
    bibliography = get_bibliography([entry_one])
    assert entry_one in bibliography
    assert entry_two not in bibliography


def test_get_entries(get_bibliography):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.get_entries` method."""
    bibliography = get_bibliography()
    assert bibliography.get_entries() == bibliography.adapter.get_entries()


@pytest.mark.parametrize(
    'sort, reverse, expected', (
        (lambda e: e.year, False, [1, 2, 3, 4]),
        (lambda e: e.year, True, [4, 3, 2, 1]),
        (lambda e: (e.author, e.year), False, [2, 4, 1, 3]),
        (lambda e: (e.author, e.year), True, [3, 1, 4, 2]),
    )
)
def test_get_entries_sort(get_bibliography, sort, reverse, expected):
    """Test :meth:`biblary.bibliography.bibliography.Bibliography.get_entries` using ``sort`` and ``reverse``."""
    bibliography = get_bibliography()
    assert [entry.identifier for entry in bibliography.get_entries(sort=sort, reverse=reverse)] == expected


@pytest.mark.parametrize(
    'sort, reverse, expected', (
        (lambda e: e.year, False, [1, 2, 3, 4]),
        (lambda e: e.year, True, [4, 3, 2, 1]),
        (lambda e: (e.author, e.year), False, [2, 4, 1, 3]),
        (lambda e: (e.author, e.year), True, [3, 1, 4, 2]),
    )
)
def test_sort(get_bibliography, sort, reverse, expected):
    """Test sorting the entries directly by iterating over the bibliography as a collection."""
    bibliography = get_bibliography()
    assert [entry.identifier for entry in sorted(bibliography.values(), key=sort, reverse=reverse)] == expected


@pytest.mark.parametrize(
    'entry',
    (BibliographyEntry(entry_type='article', identifier='123'), '{"entry_type": "article", "identifier": "123"}')
)
def test_add_entry(get_bibliography, entry):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.add_entry` method."""
    bibliography = get_bibliography()
    added = bibliography.add_entry(entry)
    assert added in bibliography


def test_add_entry_excepts(get_bibliography):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.add_entry` method when it excepts."""
    bibliography = get_bibliography()

    with pytest.raises(BibliographicEntryParsingError):
        bibliography.add_entry('invalid-content')

    with pytest.raises(DuplicateEntryError):
        bibliography.add_entry(bibliography.get_entries()[0])


def test_save(filepath_bibtex):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.save` method."""
    entry = BibliographyEntry('article', identifier='1', year='1901', author='M. Planck')
    bibliography = Bibliography(BibtexBibliography(filepath_bibtex))
    clone = Bibliography(BibtexBibliography(filepath_bibtex))

    added = bibliography.add_entry(entry)
    assert added in bibliography
    assert added not in clone

    bibliography.save()
    clone = Bibliography(BibtexBibliography(filepath_bibtex))
    assert added in bibliography
    assert added in clone
