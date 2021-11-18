"""
Example project settings, stripped down to
the minimum required for the lb health check
"""

import os
from secrets import choice
from string import ascii_letters

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Since this isn't a real project, generate a random secret key so
# the Github leak detector doesn't yell at me
SECRET_KEY = ''.join(choice(ascii_letters) for _ in range(64))

DEBUG=True

# The ALIVENESS_URL will bypass the entire Django URL system
# and serve the health check URL. This could also be a set or a list.
ALIVENESS_URL = "/health-check/"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # The lb_health_check doesn't need to be in installed_apps,
    # but doing so allows its unit tests to be run
    'lb_health_check',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # AliveCheck needs to be as high as possible below SecurityMiddlware
    # and absolutely above CommonMiddleware.
    'lb_health_check.middleware.AliveCheck',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'example.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ":memory:",
    }
}

STATIC_URL = '/static/'