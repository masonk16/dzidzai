import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    """
    Inherits from the Channels WebsocketConsumer class
    to implement a basic WebSocket consumer.
    """

    def connect(self):
        """Called when a new connection is received."""
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # accept connection
        self.accept()

    def disconnect(self, close_code):
        """
        Called when the socket closes.
        Pass is used because there is no need to implement
         any action when a client closes the connection.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    def receive(self, text_data):
        """Called whenever data is received."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))
