"""
WSGI config for phonebook project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phonebook.settings')

application = get_wsgi_application() 