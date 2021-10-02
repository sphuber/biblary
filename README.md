# Biblary


## Installation

The recommended way of installing is using `pip`:

```bash
pip install biblary
```

## Get started

First, make sure the application is added to the `INSTALLED_APPS` in your project settings:
```python
# settings.py
INSTALLED_APPS = (
    ...
    'biblary',
)
```
Next, add the URLs to your project:
```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('biblary/', include('biblary.urls', namespace='biblary')),
]
```
Finally, the adapter to the bibliography backend needs to be configured.
For example, to serve the contents of a file containing BibTeX entries, use the `BibtexBibliography` adapter:
```python
# settings.py
import pathlib

BIBLARY_BIBLIOGRAPHY_ADAPTER = 'biblary.bibliography.adapter.bibtex.BibtexBibliography'
BIBLARY_BIBLIOGRAPHY_ADAPTER_CONFIGURATION = {
    'filepath': pathlib.Path('/some/path/to/bibliography.bib')
}
```
The `filepath` is the only required key for the configuration and should be a `pathlib.Path` object pointing to the BibTeX file.

## Available adapters

### `BibtexBibliography`

This adapter is designed to serve the contents of a file containing [BibTeX](http://www.bibtex.org/Format/) entries.

#### Configuration parameters

* `filepath`: a `pathlib.Path` object that points to the BibTeX file containing the bibliographic entries.


## Writing custom adapter

To provide an adapter to a custom bibliography backend, one should implement the `biblary.bibliography.adapter.abstract.BibliographyAdapter` class:
```python
# -*- coding: utf-8 -*-
import typing as t

from biblary.bibliography.adapter import BibliographyAdapter
from biblary.bibliography.entry import BibliographyEntry


class CustomBibliographyAdapter(BibliographyAdapter):
    """Implementation of a ``BibliographyAdapter``."""

    def __init__(self, *args, **kwargs):
        """Construct a new instance and configure the adapter."""
        super().__init__(*args, **kwargs)

    def get_entries(self) -> t.List[BibliographyEntry]:
        """Return the list of bibliography entries."""
```
The constructor should define what keyword arguments it should take in order to configure the adapter.
The keyword arguments that are specified for the `BIBLARY_BIBLIOGRAPHY_ADAPTER_CONFIGURATION` will be passed to the constructor of the adapter when the bibliography is loaded.
Finally, the `get_entries` method should be implemented.
It should return a list of `biblary.bibliography.entry.BiliographyEntry` instances, one for each entry in the bibliography.


## Configuration

### `BIBLARY_BIBLIOGRAPHY_MAIN_AUTHOR_PATTERNS`

This setting takes a tuple of regex patterns, for example

```python
BIBLARY_BIBLIOGRAPHY_MAIN_AUTHOR_PATTERNS = ('Paul Dirac', r'.*Dirac')
```

The template tag `main_author_class` will use this setting to determine if the author that it is passed is considered a main author.
If that is the case, the string defined by the `BIBLARY_BIBLIOGRAPHY_MAIN_AUTHOR_CLASS` setting is returned.
This can be used in the `index` template as follows:

```jinja
{% for entry in entries %}
<div class="biblary-entry-authors">
    {% for author in entry.author %}
    <span class="biblary-entry-author {% main_author_class author %}">{{ author }}</span>
    {% endfor %}
</div>
{% endfor %}
```

Any author that will match any of the patterns specified by the setting, will get the additional class.

### `BIBLARY_BIBLIOGRAPHY_MAIN_AUTHOR_CLASS`

Returned by the `main_author_class` tag if the specified author matches any of the patterns defined by the `BIBLARY_BIBLIOGRAPHY_MAIN_AUTHOR_PATTERNS` setting.
Default is `biblary-entry-author-main`.
