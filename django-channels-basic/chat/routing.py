from django.urls import path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/chat/)', ChatConsumer.as_asgi()),
]