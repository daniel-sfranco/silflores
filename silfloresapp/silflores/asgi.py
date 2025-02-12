import os
import django.core.asgi as dj_asgi #type:ignore
import channels.routing #type:ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silflores.settings')

application = dj_asgi.get_asgi_application()
application = channels.routing.get_default_application()
