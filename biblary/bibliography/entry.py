# -*- coding: utf-8 -*-
"""Module with data class that represents an entry in a bibliography."""
from dataclasses import dataclass
import typing as t

__all__ = ('BibliographyEntry',)


@dataclass
class BibliographyEntry:
    """Class representing an entry in a bibliography."""

    entry_type: str
    identifier: str
    author: t.Optional[str] = None
    title: t.Optional[str] = None
    publisher: t.Optional[str] = None
    journal: t.Optional[str] = None
    volume: t.Optional[int] = None
    issue: t.Optional[int] = None
    pages: t.Optional[str] = None
    month: t.Optional[int] = None
    year: t.Optional[int] = None
    keyword: t.Optional[str] = None
    url: t.Optional[str] = None
    doi: t.Optional[str] = None
