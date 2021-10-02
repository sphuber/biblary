# -*- coding: utf-8 -*-
"""Abstract class that represents the interface to a file store of files associated with bibliographic entries."""
import abc
import enum
import io
import typing as t

from ..entry import BibliographyEntry

__all__ = ('AbstractStorage', 'FileType')


class FileType(enum.Enum):
    """Enumeration with the supported file types.

    Each bibliographic entry can have one file for each of these types.
    """

    MANUSCRIPT = 'manuscript'
    PREPRINT = 'preprint'
    SUPPLEMENTARY = 'supplementary'


class AbstractStorage(abc.ABC):
    """Abstract class that represents the interface to a file store of files associated with bibliographic entries."""

    @abc.abstractmethod
    def get_file(self, entry: BibliographyEntry, file_type: FileType) -> bytes:
        """Return the byte content of a file with the given type for the given bibliographic entry.

        :param entry: the :class:`biblary.bibliographic.entry.BibliographicEntry` for which to retrieve the file.
        :param file_type: the file type to retrieve for the given entry.
        :raises ``FileNotFoundError``: if the file of the given type does not exist for the given entry.
        """

    @abc.abstractmethod
    def put_file(self, content: t.Union[io.BytesIO, bytes], entry: BibliographyEntry, file_type: FileType) -> None:
        """Write the given byte content for the given bibliographic entry and file type.

        :param entry: the :class:`biblary.bibliographic.entry.BibliographicEntry` for which to retrieve the file.
        :param file_type: the file type to retrieve for the given entry.
        :raises ``TypeError``: if the ``content`` is not a byte-stream or pure bytes.
        """

    @abc.abstractmethod
    def exists(self, entry: BibliographyEntry, file_type: FileType) -> bool:
        """Return whether the file with the given type for the given bibliographic entry exists.

        :param entry: the :class:`biblary.bibliographic.entry.BibliographicEntry` for which to retrieve the file.
        :param file_type: the file type to retrieve for the given entry.
        :returns: True if the file exists and False otherwise.
        """
