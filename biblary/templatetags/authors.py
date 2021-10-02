# -*- coding: utf-8 -*-
"""Module with template tags operating on the authors of bibliographic entries."""
import re
import typing as t

from django import template

register = template.Library()


@register.simple_tag()
def main_author_class(author: str) -> t.Optional[str]:
    """Return whether the given author matches any of the patterns in the ``BIBLIOGRAPHY_MAIN_AUTHOR_PATTERS``.

    :param author: the author.
    """
    from biblary.settings import settings

    patterns = settings.bibliography_main_author_patterns

    if not isinstance(patterns, tuple):
        raise TypeError('invalid configuration: setting `BIBLIOGRAPHY_MAIN_AUTHOR_PATTERS` should be a tuple.')

    if patterns and any(re.match(pattern, author) for pattern in patterns):
        return settings.bibliography_main_author_class

    return None
