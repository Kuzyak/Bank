"""
WSGI config for newsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
#activate_this = '/home/ubuntu/Bank/myvenv/bin/activate_this.py'
#exec(compile(open(activate_this,"rb").read(),activate_this, 'exec'), dict(__file__=activate_this))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsite.settings")

application = get_wsgi_application()
