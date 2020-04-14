from djnago.urls import path
from . import consumers

websocket_urlpatterns = [
    path('wss/chat/<str:room_id>/', consumers.ChatConsumer),
]