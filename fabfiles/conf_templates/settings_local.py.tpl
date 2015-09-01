import settings
import os

#DEBUG = False
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%(db_name)s',                              # Or path to database file if using sqlite3.
        'USER': '%(db_user)s',                              # Not used with sqlite3.
        'PASSWORD': '%(db_pass)s',                          # Not used with sqlite3.
        'HOST': '127.0.0.1',                                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                     # Set to empty string for default. Not used with sqlite3.
    }
}
