# -*- coding: utf-8 -*-
"""Implementation of :class:`biblary.bibliography.adapter.BibliographyAdapter` that builds from a Bibtex file."""
import pathlib
import typing as t

from ..entry import BibliographyEntry
from .abstract import BibliographyAdapter


class BibtexBibliography(BibliographyAdapter):
    """Implementation of :class:`biblary.bibliography.adapter.BibliographyAdapter` that builds from a Bibtex file."""

    def __init__(self, filepath: pathlib.Path, *_, **__):
        """Construct a new instance.

        :param filepath: absolute filepath to a Bibtex file containing the bibliographic entries.
        """
        self.filepath = filepath

    @staticmethod
    def _transform_authors(record):
        """Reverse the ordering of the author parts and join with normal spaces.

        This will essentially transform "Oppenheimer, Robert" into "Robert Oppenheimer".
        """
        record['author'] = [' '.join(author.split(',')[::-1]) for author in record['author']]
        return record

    def _customize_record(self, record):
        """Apply a set of transformations on the provided record."""
        from bibtexparser import customization

        transformers = (
            customization.convert_to_unicode,
            customization.keyword,
            customization.page_double_hyphen,
            customization.type,
            customization.author,
            self._transform_authors,
        )

        for transformer in transformers:
            record = transformer(record)

        return record

    def get_entries(self) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries."""
        from bibtexparser import load
        from bibtexparser.bparser import BibTexParser

        parser = BibTexParser()
        parser.customization = self._customize_record

        entries = []

        with self.filepath.open() as handle:
            database = load(handle, parser=parser)

        for entry in database.entries:
            entries.append(
                BibliographyEntry(
                    entry_type=entry['ENTRYTYPE'],
                    identifier=entry['ID'],
                    author=entry.get('author', None),
                    title=entry.get('title', None),
                    publisher=entry.get('publisher', None),
                    journal=entry.get('journal', None),
                    volume=entry.get('volume', None),
                    issue=entry.get('issue', None),
                    pages=entry.get('pages', None),
                    month=entry.get('month', None),
                    year=entry.get('year', None),
                    keyword=entry.get('keyword', None),
                    url=entry.get('url', None),
                    doi=entry.get('doi', None),
                )
            )

        return entries
