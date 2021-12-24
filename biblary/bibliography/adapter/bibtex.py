# -*- coding: utf-8 -*-
"""Implementation of :class:`biblary.bibliography.adapter.BibliographyAdapter` that builds from a Bibtex file."""
import dataclasses
import io
import pathlib
import shutil
import tempfile
import typing as t

from bibtexparser import customization, load
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

from ..entry import BibliographyEntry
from ..exceptions import BibliographicEntryParsingError
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
        record['author'] = [' '.join(author.split(',')[::-1]).strip() for author in record['author']]
        return record

    def _customize_record(self, record):
        """Apply a set of transformations on the provided record."""
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

    @staticmethod
    def _convert_entry(entry: t.Dict[str, t.Any]) -> BibliographyEntry:
        """Convert an entry parsed by ``bibtexparser`` into a ``BibliographyEntry``.

        :param entry: a dictionary representing the bibliographic entry.
        :return: the converted entry.
        """
        return BibliographyEntry(
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

    def get_entries(self) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries.

        :return: list of bibliographic entries.
        :raises :class:`bibliography.exceptions.BibliographicEntryParsingError`: if parsing fails.
        """
        parser = BibTexParser()
        parser.customization = self._customize_record

        with self.filepath.open() as handle:
            database = load(handle, parser=parser)

        if not database.entries:
            raise BibliographicEntryParsingError('failed to parse bibliographic entry from provided content.')

        return [self._convert_entry(entry) for entry in database.entries]

    def parse_entry(self, content: str) -> BibliographyEntry:
        """Parse a new bibliographic entry from a string.

        :param content: the entry in string form.
        :return: the parsed bibliographic entry.
        :raises :class:`bibliography.exceptions.BibliographicEntryParsingError`: if parsing fails.
        """
        parser = BibTexParser()
        parser.customization = self._customize_record

        database = load(io.StringIO(content), parser=parser)

        if not database.entries:
            raise BibliographicEntryParsingError('failed to parse bibliographic entry from provided content.')

        return self._convert_entry(database.entries[0])

    def save_entries(self, entries: t.List[BibliographyEntry]) -> None:
        """Save the list of entries to the bibliography.

        :param entries: list of bibliographic entries to write to the original bibliographic file.
        """
        database = BibDatabase()
        writer = BibTexWriter()
        writer.indent = '    '

        for entry in entries:
            dictionary = {
                'ENTRYTYPE': entry.entry_type,
                'ID': entry.identifier,
            }
            for field in dataclasses.fields(entry):
                if field.name in {'identifier', 'entry_type'}:
                    continue

                value = getattr(entry, field.name)

                if value is not None:
                    if field.name == 'author':
                        authors = ' and '.join([author.strip() for author in value])
                        dictionary[field.name] = authors
                    else:
                        dictionary[field.name] = value

            database.entries.append(dictionary)

        with tempfile.NamedTemporaryFile('w') as handle:
            handle.write(writer.write(database))
            handle.flush()
            shutil.copy(handle.name, self.filepath)
