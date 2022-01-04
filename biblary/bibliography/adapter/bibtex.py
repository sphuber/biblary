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

    @classmethod
    def _customize_record(cls, record):
        """Apply a set of transformations on the provided record."""
        transformers = (
            customization.convert_to_unicode,
            customization.keyword,
            customization.page_double_hyphen,
            customization.type,
            customization.author,
            cls._transform_authors,
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

    @classmethod
    def _parse_bibliography(cls, filelike: t.TextIO) -> t.List[BibliographyEntry]:
        """Parse bibliographic entries from a text stream that should contain a ``.bib`` bibliography.

        :param filelike: a filelike object containing the content to parse.
        :return: list of parsed bibliographic entries.
        :raises :class:`bibliography.exceptions.BibliographicEntryParsingError`: if parsing fails.
        """
        parser = BibTexParser()
        parser.customization = cls._customize_record

        database = load(filelike, parser=parser)

        if not database.entries or not database.entries[0]:
            raise BibliographicEntryParsingError('failed to parse entries from bibliography.')

        return [cls._convert_entry(entry) for entry in database.entries]

    @classmethod
    def parse_entry(cls, content: str) -> BibliographyEntry:
        """Parse a new bibliographic entry from a string.

        :param content: the entry in string form.
        :return: the parsed bibliographic entry.
        :raises :class:`bibliography.exceptions.BibliographicEntryParsingError`: if parsing fails.
        """
        return cls._parse_bibliography(io.StringIO(content))[0]

    def get_entries(self) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries.

        :return: list of bibliographic entries.
        :raises :class:`bibliography.exceptions.BibliographicEntryParsingError`: if parsing fails.
        """
        with self.filepath.open() as handle:
            return self._parse_bibliography(handle)

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
