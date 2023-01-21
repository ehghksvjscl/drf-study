from django.urls import path
from app.consumers import EchoConsumer, LiveBlogConsumer

websocket_urlpatterns = [
    path('ws/liveblog/', LiveBlogConsumer.as_asgi()),
    path('ws/echo/', EchoConsumer.as_asgi()),
]