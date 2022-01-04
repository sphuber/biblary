# -*- coding: utf-8 -*-
"""Module with form and form field definitions."""
from django import forms

from .bibliography.storage import FileType

__all__ = ('BibliographyUploadFileForm', 'BibliographyUploadEntryForm')


class FileTypeField(forms.TypedChoiceField):
    """Form field that provides a choice of a :class:`biblary.bibliography.storage.FileType`."""

    def __init__(self, *, choices=None, coerce=None, empty_value=None, **kwargs):
        """Construct a new instance.

        The ``choices``, ``coerce`` and ``empty_value`` argument of the ``forms.TypedChoiceField`` base class static and
        automatically determined from the :class:`biblary.bibliography.storage.FileType` enum. The constructor will
        raise a ``ValueError`` if they are specified.

        :raises ValueError: if ``choices``, ``coerce`` or ``empty_value`` are defined.
        """
        super().__init__(**kwargs)

        for arg in [choices, coerce, empty_value]:
            if arg is not None:
                raise ValueError(f'`{arg.__name__}` cannot be changed for the `FileTypeField`.')

        self.choices = [(file_type.value, file_type.value) for file_type in FileType]
        self.coerce = FileType
        self.empty_value = ()


class BibliographyUploadFileForm(forms.Form):
    """Form to upload a file of a given type for the specified bibligraphic entry.

    .. note:: The choices of the ``entry_identifier`` have to be specified in the view that presents the form because
        those should depend on the :class:`biblary.bibliography.Bibliography` that is configured and loaded. The values
        should correspond to the entries of the :class:`biblary.bibliography.entry.BibliographicEntry`'s.
    """

    entry_identifier = forms.ChoiceField(label='Entry')
    file_type = FileTypeField(label='Type')
    content = forms.FileField(label='File')


class BibliographyUploadEntryForm(forms.Form):
    """Form to upload a bibligraphic entry."""

    content = forms.CharField(label='', widget=forms.Textarea())
