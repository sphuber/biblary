# -*- coding: utf-8 -*-
"""Abstract class representing the backend to a bibliography."""
import abc
import typing as t

from ..entry import BibliographyEntry


class BibliographyAdapter(abc.ABC):
    """Abstract class representing the backend to a bibliography."""

    @abc.abstractmethod
    def get_entries(self) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries."""

    @classmethod
    @abc.abstractmethod
    def parse_entry(cls, content: str) -> BibliographyEntry:
        """Parse a new bibliographic entry from a string.

        :param content: the entry in string form.
        :return: the parsed bibliographic entry.
        :raises :class:`bibliography.exceptions.BibliographicEntryParsingError`: if parsing fails.
        """

    @classmethod
    @abc.abstractmethod
    def write_entry(cls, entry: BibliographyEntry, stream: t.TextIO) -> None:
        """Write a bibliographic entry formatted as text to the given stream.

        :param entry: bibliographic entry to write formatted to stream.
        """

    @abc.abstractmethod
    def save_entries(self, entries: t.List[BibliographyEntry]) -> None:
        """Save the list of entries to the bibliography."""
