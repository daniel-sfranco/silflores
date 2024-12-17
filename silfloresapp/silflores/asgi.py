import os
import django.core.asgi as dj_asgi
import channels.routing #type:ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = dj_asgi.get_asgi_application()
application = channels.routing.get_default_application()
