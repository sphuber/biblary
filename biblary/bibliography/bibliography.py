# -*- coding: utf-8 -*-
"""Module with class that represents a bibliography."""
import typing as t

from .adapter import BibliographyAdapter
from .entry import BibliographyEntry


class Bibliography:
    """Collection of bibliographic entries.

    Entries are represented by instances of the :class:`biblary.bibliography.entry.BibliographyEntry` class. The parsing
    of the bibliographic entries is provided by an instance of :class:`biblary.bibliography.adapter.BibliographyAdapter`
    which is passed to the constructor.
    """

    def __init__(self, adapter: BibliographyAdapter):
        """Construct a new bibliography instance.

        :param adapter: bibliography adapter that provides access to the bibliography backend.
        """
        if not isinstance(adapter, BibliographyAdapter):
            raise TypeError(f'`adapter` should be an instance of `BibliographyAdapter`, but got: `{adapter}`.')

        self.adapter: BibliographyAdapter = adapter
        self._entries: t.Optional[t.List[BibliographyEntry]] = None

    def get_entries(
        self,
        sort: t.Callable[[BibliographyEntry], int] = None,
        reverse: bool = False,
    ) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries.

        :param sort: optional lambda to sort the returned list of entries.
        :param reverse: whether to reverse the order of the sorting if `sort` is specified.
        """
        if self._entries is None:
            self._entries = self.adapter.get_entries()

        if sort is not None:
            self._entries.sort(key=sort, reverse=reverse)

        return self._entries
