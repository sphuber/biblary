# -*- coding: utf-8 -*-
"""Module that defines the views of this application."""
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.http.response import Http404, HttpResponse
from django.views.generic import TemplateView, View

from .bibliography.storage import FileType
from .utils import BibliographyMixin


class BiblaryIndexView(BibliographyMixin, TemplateView):
    """View with index of bibliography contents."""

    template_name = 'biblary/index.html'

    def get_context_data(self, **kwargs):
        """Add the entries of the bibliography to the context."""
        bibliography = self.get_bibliography()

        context = super().get_context_data(**kwargs)
        context['entries'] = []

        for entry in bibliography.get_entries(sort=lambda entry: entry.year, reverse=True):

            if bibliography.storage is not None:
                entry.files = {file_type.value: bibliography.storage.exists(entry, file_type) for file_type in FileType}

            context['entries'].append(entry)

        return context


class BiblaryFileView(BibliographyMixin, View):
    """View that serves a file stored for a bibliographic entry."""

    def get(self, _, *__, **___) -> HttpResponse:
        """Return the byte content of the file for the specified bibliographic entry and file type.

        :returns :class:`django.http.response.HttpResponse`: if the file exists for the specified entry and file type.
        :raises :class:`django.core.exceptions.SuspiciousOperation`: if the requested file type does not exist.
        :raises :class:`django.core.exceptions.Http404`: if the bibliographic entry does not exist, or it
            does but the requested file does not exist.
        """
        entry_identifier = self.kwargs['identifier']
        file_type = self.kwargs['file_type']

        bibliography = self.get_bibliography()

        if bibliography.storage is None:
            raise ImproperlyConfigured('No file storage has been configured.')

        try:
            file_type = FileType(self.kwargs['file_type'])
        except ValueError as exc:
            raise SuspiciousOperation(f'The requested file type `{file_type}` is invalid.') from exc

        try:
            entry = bibliography[entry_identifier]
        except KeyError as exc:
            raise Http404(f'The requested bibliographic entry `{entry_identifier}` does not exist.') from exc

        try:
            content = bibliography.storage.get_file(entry, file_type)
        except FileNotFoundError as exc:
            raise Http404(f'The requested file `{entry_identifier}:{file_type.value}` does not exist.') from exc

        return HttpResponse(
            content,
            headers={
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'attachment; filename="{file_type.value}.pdf"',
            }
        )
