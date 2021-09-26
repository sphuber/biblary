# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Tests for the :mod:`biblary.bibliography.bibliography` module."""
import typing as t

import pytest

from biblary.bibliography.adapter.abstract import BibliographyAdapter
from biblary.bibliography.bibliography import Bibliography
from biblary.bibliography.entry import BibliographyEntry
from biblary.bibliography.exceptions import InvalidBibliographyError


class MockAdapter(BibliographyAdapter):
    """Mock implementation of :class:`biblary.bibliography.adapter.abstract.BibliographyAdapter`."""

    def __init__(self, *args, entries=None, **kwargs):
        """Construct new instance for a list of entries."""
        super().__init__(*args, **kwargs)
        self._entries = entries

    def get_entries(self):
        """Return the list of bibliographic entries for this bibliography."""
        return self._entries


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
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__get_item` method."""
    bibliography = get_bibliography(entries)

    for entry in entries:
        assert bibliography[entry.identifier] is entry


@pytest.mark.parametrize('entries', (([]), ([BibliographyEntry('a', 1), BibliographyEntry('a', 2)])))
def test_iter(get_bibliography, entries):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__iter` method."""
    bibliography = get_bibliography(entries)

    for identifier in bibliography:
        assert isinstance(bibliography[identifier], BibliographyEntry)


@pytest.mark.parametrize('entries', (([]), ([BibliographyEntry('a', 1), BibliographyEntry('a', 2)])))
def test_len(get_bibliography, entries):
    """Test the :meth:`biblary.bibliography.bibliography.Bibliography.__len` method."""
    bibliography = get_bibliography(entries)
    assert len(bibliography) == len(entries)


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
