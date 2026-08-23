"""
ASGI config for siksha_sahayak project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siksha_sahayak.settings')

application = get_asgi_application()
