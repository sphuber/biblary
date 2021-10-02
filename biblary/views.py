# -*- coding: utf-8 -*-
"""Module that defines the views of this application."""
import typing as t

from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.forms import Form
from django.http.response import Http404, HttpResponse
from django.views.generic import FormView, TemplateView, View

from .bibliography.storage import FileType
from .forms import BibliographyUploadFileForm
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

        try:
            bibliography = self.get_bibliography(storage_required=True)
        except ImproperlyConfigured as exc:
            raise Http404('No files are available for the current configuration.') from exc

        assert bibliography.storage is not None

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


class BiblaryUploadView(BibliographyMixin, FormView):
    """View to upload a file of a give file type for a bibliographic entry."""

    form_class = BibliographyUploadFileForm
    success_url = 'upload'
    template_name = 'biblary/upload.html'

    def get_form(self, form_class: Form = None) -> t.Optional[None]:
        """Return an instance of the form to be used in this view if a file storage has been configured.

        Before returning the form, the choices of the ``entry_identifier`` are defined based on the configured and
        loaded bibliography. To upload files, a file storage is required. If no file storage is configured, ``None`` is
        returned instead of the form.
        """
        try:
            bibliography = self.get_bibliography(storage_required=True)
        except ImproperlyConfigured:
            return None
        else:
            form = super().get_form(form_class)
            form.fields['entry_identifier'].choices = [(e.identifier, e.identifier) for e in bibliography.values()]
            return form

    def post(self, request, *args, **kwargs):
        """Validate that a bibliography with file storage has been configured and then forward the request.

        If no bibliography with file storage has been configured, forward to the ``get`` method which should display
        that the upload functionality is disables since no file storage is configured.
        """
        try:
            self.get_bibliography(storage_required=True)
        except ImproperlyConfigured:
            return super().get(request, *args, **kwargs)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form: BibliographyUploadFileForm):
        """Write the uploaded content to the file storage configured for the loaded bibliography.

        .. note:: This method assumes that a bibliography including a file storage has been configured. This should have
            been checked in the ``post`` method of this view.
        """
        content = form.cleaned_data['content']
        file_type = form.cleaned_data['file_type']
        entry_identifer = form.cleaned_data['entry_identifier']

        bibliography = self.get_bibliography(storage_required=True)
        entry = bibliography[entry_identifer]
        assert bibliography.storage is not None

        with content.open('rb') as handle:
            bibliography.storage.put_file(handle, entry, file_type)

        return super().form_valid(form)
