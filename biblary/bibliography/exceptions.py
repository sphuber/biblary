# -*- coding: utf-8 -*-
"""Module with custom exceptions."""


class InvalidBibliographyError(ValueError):
    """Raised when :class:`bibliography.bibliography.Bibliography` is constructed with an invalid bibliography."""
