

def pytest_configure():
    from django.conf import settings
    import sys

    try:
        import django  # NOQA
    except ImportError:
        print("Error: missing test dependency:")
        print("  django library is needed to run test suite")
        print("  you can install it with 'pip install django'")
        print("  or use tox to automatically handle test dependencies")
        sys.exit(1)
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests.
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'navutils',
            'tests.test_app',
        ],
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        # Django replaces this, but it still wants it. *shrugs*
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MEDIA_ROOT='/tmp/django_extensions_test_media/',
        MEDIA_PATH='/media/',
        ROOT_URLCONF='tests.test_app.urls',
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    # insert your TEMPLATE_DIRS here
                ],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                        # list if you haven't customized them:
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        SECRET_KEY = 'not secure only for testing',
    )
