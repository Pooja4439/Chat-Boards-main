from django.urls import re_path,path
from .consumers import ChatConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

ws_urlpatterns = [path("ws/board/<str:board_name>/connect", ChatConsumer.as_asgi())]