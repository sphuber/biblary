# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Tests for the :mod:`biblary.bibliography.storage.file_system` module."""
import pytest

from biblary.bibliography.entry import BibliographyEntry
from biblary.bibliography.storage import FileType
from biblary.bibliography.storage.file_system import FileSystemStorage


@pytest.fixture
def file_storage(tmp_path):
    """Return an instance of :class:`biblary.bibliography.storage.file_system.FileSystemStorage`."""
    return FileSystemStorage(filepath=tmp_path)


@pytest.fixture
def write_file():
    """Write binary content to a file storage for the given entry and file type."""

    def _fixture(
        file_storage: FileSystemStorage, entry: BibliographyEntry, file_type: FileType, content: bytes
    ) -> None:
        """Write binary content to a file storage for the given entry and file type.

        :param file_storage: the file storage to write to.
        :param entry: the bibliographic entry.
        :param file_type: the file type.
        :param content: the byte content to write to disk.
        """
        filepath = file_storage.get_filepath(entry, file_type)
        filepath.parent.mkdir(exist_ok=True, parents=True)
        filepath.write_bytes(content)

    return _fixture


def test_get_file(file_storage):
    """Test the :meth:`biblary.bibliography.storage.file_system.FileSystemStorage.get_file` method."""
    entry = BibliographyEntry('article', 1)
    file_type = FileType.MANUSCRIPT
    content = b'test-content'

    filepath = file_storage.get_filepath(entry, file_type)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    filepath.write_bytes(content)

    assert file_storage.get_file(entry, file_type) == content


def test_get_file_non_existing(file_storage):
    """Test the :meth:`biblary.bibliography.storage.file_system.FileSystemStorage.get_file` method.

    Test the method raises when the requested file does not exist.
    """
    entry = BibliographyEntry('article', 1)

    with pytest.raises(FileNotFoundError):
        file_storage.get_file(entry, FileType.MANUSCRIPT)


def test_get_file_invalid_type(file_storage):
    """Test the :meth:`biblary.bibliography.storage.file_system.FileSystemStorage.get_file` method.

    Test the method raises when receiving an invalid file type.
    """
    entry = BibliographyEntry('article', 1)

    with pytest.raises(TypeError, match=r'file_type `.*` is not a valid `FileType`.'):
        file_storage.get_file(entry, 'non-existing-type')


def test_exists(file_storage, write_file):
    """Test the :meth:`biblary.bibliography.storage.file_system.FileSystemStorage.exists` method."""
    entry = BibliographyEntry('article', 1)
    file_type = FileType.MANUSCRIPT

    write_file(file_storage, entry, FileType.MANUSCRIPT, b'')

    assert file_storage.exists(entry, file_type)
    assert not file_storage.exists(entry, FileType.SUPPLEMENTARY)
