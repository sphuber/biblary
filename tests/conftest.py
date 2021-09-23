# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Module with unit test fixtures."""
import contextlib
import pathlib
import typing as t

import pytest


@pytest.fixture
def override_settings() -> t.Callable:
    """Fixture to change a configuration setting for the duration of the test."""

    @contextlib.contextmanager
    def _override_settings(**kwargs) -> None:
        from django.test.utils import override_settings

        with override_settings(**{f'BIBLARY_{key.upper()}': value for key, value in kwargs.items()}):
            yield

    return _override_settings


@pytest.fixture
def filepath_bibtex(tmp_path) -> pathlib.Path:
    """Return the filepath to a Bibtex file."""
    filepath_source = pathlib.Path(__file__).parent / 'fixtures' / 'bibliography' / 'basic.bib'
    filepath_target = tmp_path / 'bibliography.bib'

    with filepath_target.open('wb') as handle:
        handle.write(filepath_source.read_bytes())
        handle.flush()

    yield filepath_target
