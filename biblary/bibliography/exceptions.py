# -*- coding: utf-8 -*-
"""Module with custom exceptions."""


class BibliographicEntryParsingError(ValueError):
    """Raised when :class:`bibliography.adapter.abstract.BibliographyAdapter.parse_entry` fails to parse the entry."""


class InvalidBibliographyError(ValueError):
    """Raised when :class:`bibliography.bibliography.Bibliography` is constructed with an invalid bibliography."""
