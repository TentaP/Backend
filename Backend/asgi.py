"""
ASGI config for Backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.core.asgi import get_asgi_application
from tentap.ws.consumers import EchoConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    {
        "http": django_asgi_app,
        "websocket": URLRouter(path("ws/", RealtimeConsumer.as_asgi())),
    }
})

