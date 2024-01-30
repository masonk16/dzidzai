import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Inherits from the Channels WebsocketConsumer class
    to implement a basic WebSocket consumer.
    """

    async def connect(self):
        """Called when a new connection is received."""
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the socket closes.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        """Called whenever data is received."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': timezone.now().isoformat(),
            }
        )

    async def chat_message(self, event):
        """
        Receive message from room group and
        send message to WebSocket.
        """
        await self.send(text_data=json.dumps(event))
