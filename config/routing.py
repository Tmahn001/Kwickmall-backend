from django.urls import re_path

from api.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
    #re_path(r'ws/test/$', consumers.TestConsumer.as_asgi()),
]


