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
