# -*- coding: utf-8 -*-
"""Implementation of :class:`biblary.bibliography.storage.AbstractStorage` that stores on the local file system."""
import hashlib
import pathlib

from ..entry import BibliographyEntry
from .abstract import AbstractStorage, FileType

__all__ = ('FileSystemStorage',)


class FileSystemStorage(AbstractStorage):
    """Implementation of :class:`biblary.bibliography.storage.AbstractStorage` that builds from a Bibtex file."""

    def __init__(self, filepath: pathlib.Path, *_, **__):
        """Construct a new instance.

        :param filepath: absolute filepath to the base folder where files will be stored.
        """
        self.filepath = pathlib.Path(filepath)

    @staticmethod
    def validate_file_type(file_type):
        """Validate the ``file_type``.

        :raises ``TypeError``: if the given ``file_type`` is not a valid ``FileType``.
        """
        if not isinstance(file_type, FileType):
            raise TypeError(f'file_type `{file_type}` is not a valid `FileType`.')

    def get_filepath(self, entry: BibliographyEntry, file_type: FileType) -> pathlib.Path:
        """Return the byte content of a file with the given type for the given bibliographic entry.

        :param entry: the :class:`biblary.bibliographic.entry.BibliographicEntry` for which to retrieve the file.
        :param file_type: the file type to retrieve for the given entry.
        :returns: the absolute filepath where the file should be stored if it exists.
        """
        self.validate_file_type(file_type)

        doi_hash = hashlib.sha256(str(entry.identifier).encode('utf-8')).hexdigest()

        if isinstance(file_type, FileType):
            filename = file_type.value
        else:
            filename = file_type

        return self.filepath / doi_hash / filename

    def get_file(self, entry: BibliographyEntry, file_type: FileType) -> bytes:
        """Return the byte content of a file with the given type for the given bibliographic entry.

        :param entry: the :class:`biblary.bibliographic.entry.BibliographicEntry` for which to retrieve the file.
        :param file_type: the file type to retrieve for the given entry.
        :raises ``FileNotFoundError``: if the file of the given type does not exist for the given entry.
        :raises ``TypeError``: if the given ``file_type`` is not a valid ``FileType``.
        """
        with self.get_filepath(entry, file_type).open('rb') as handle:
            return handle.read()

    def exists(self, entry: BibliographyEntry, file_type: FileType) -> bool:
        """Return whether the file with the given type for the given bibliographic entry exists.

        :param entry: the :class:`biblary.bibliographic.entry.BibliographicEntry` for which to retrieve the file.
        :param file_type: the file type to retrieve for the given entry.
        :returns: True if the file exists and False otherwise.
        :raises ``TypeError``: if the given ``file_type`` is not a valid ``FileType``.
        """
        return self.get_filepath(entry, file_type).exists()
