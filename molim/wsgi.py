"""
WSGI config for molim project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import dotenv
dotenv.read_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'molim.settings')

application = get_wsgi_application()
