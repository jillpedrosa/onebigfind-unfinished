# lostandfound/routing.py

from django.urls import re_path
from . import consumers  # Update to your app's consumers module

websocket_urlpatterns = [
    re_path(r'ws/some_path/$', consumers.SomeConsumer.as_asgi()),  # Update the path and consumer
]
