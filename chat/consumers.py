import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """
    Inherits from the Channels WebsocketConsumer class
    to implement a basic WebSocket consumer.
    """

    def connect(self):
        """Called when a new connection is received."""
        # accept connection
        self.accept()

    def disconnect(self, close_code):
        """
        Called when the socket closes.
        Pass is used because there is no need to implement
         any action when a client closes the connection.
        """
        pass

    # receive message from WebSocket
    def receive(self, text_data):
        """Called whenever data is received."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))
