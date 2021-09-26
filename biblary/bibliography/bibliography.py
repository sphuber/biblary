# -*- coding: utf-8 -*-
"""Module with class that represents a bibliography."""
import typing as t
from collections.abc import Mapping

from .adapter import BibliographyAdapter
from .entry import BibliographyEntry
from .exceptions import InvalidBibliographyError


class Bibliography(Mapping):
    """Collection of bibliographic entries.

    Entries are represented by instances of the :class:`biblary.bibliography.entry.BibliographyEntry` class. The parsing
    of the bibliographic entries is provided by an instance of :class:`biblary.bibliography.adapter.BibliographyAdapter`
    which is passed to the constructor.

    The class is implemented and behaves as a mapping. When iterated over it, it will return the identifiers of the
    bibliographic entries that it contains. The class can be indexed with an identifier to retrieve the corresponding
    entry from the collection.
    """

    def __init__(self, adapter: BibliographyAdapter):
        """Construct a new bibliography instance.

        :param adapter: bibliography adapter that provides access to the bibliography backend.
        """
        if not isinstance(adapter, BibliographyAdapter):
            raise TypeError(f'`adapter` should be an instance of `BibliographyAdapter`, but got: `{adapter}`.')

        self.adapter: BibliographyAdapter = adapter
        self._entries: t.Dict[str, BibliographyEntry] = self._initialize_entries()

    def __getitem__(self, key) -> BibliographyEntry:
        """Return a bibliographic entry for the given key which should correspond to the entry's identifier."""
        return self._entries[key]

    def __iter__(self) -> t.Iterator[str]:
        """Return an iterator over the bibliographic entries contained within this bibliography."""
        return iter(self._entries)

    def __len__(self) -> int:
        """Return the number of bibliographic entries contained within this bibliography."""
        return len(self._entries)

    def _initialize_entries(self) -> t.Dict[str, BibliographyEntry]:
        """Initialize the internal mapping of bibliographic entries obtained through the adapter.

        :raises :class:`biblary.exceptions.InvalidBibliographyError`: if the bibliography contains entries with
            duplicate identifiers.
        """
        entries = self.adapter.get_entries()

        if entries is None:
            return {}

        identifiers = [entry.identifier for entry in entries]

        if len(identifiers) != len(set(identifiers)):
            raise InvalidBibliographyError('the configured bibliography contains entries with duplicate identifiers.')

        return {entry.identifier: entry for entry in entries}

    def get_entries(
        self,
        sort: t.Callable[[BibliographyEntry], int] = None,
        reverse: bool = False,
    ) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries.

        :param sort: optional lambda to sort the returned list of entries.
        :param reverse: whether to reverse the order of the sorting if `sort` is specified.
        """
        if sort is not None:
            return sorted(self._entries.values(), key=sort, reverse=reverse)

        return list(self._entries.values())
