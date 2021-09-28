# -*- coding: utf-8 -*-
"""Module that abstracts the interface to a storage of files associated with bibliographic entries.

For example, this can be used to store the PDF of an article associated with a certain bibliography entry.
"""
from .abstract import AbstractStorage, FileType
from .file_system import FileSystemStorage

__all__ = ('AbstractStorage', 'FileType', 'FileSystemStorage')
