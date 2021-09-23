# -*- coding: utf-8 -*-
"""Module with settings for testing this application."""
SECRET_KEY = 'want-to-know-a-secret?'
SITE_ID = 1

DATABASES = {}

INSTALLED_APPS = ('biblary',)

MIDDLEWARE = ()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'biblary.urls'
