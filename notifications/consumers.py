# notifications/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # A user-specific group name is created to send notifications only to that user.
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}_notifications"
            self.channel_layer.group_add(self.group_name, self.channel_name)
            self.accept()

    def disconnect(self, close_code):
        # On disconnect, the user is removed from their specific group.
        if hasattr(self, 'group_name'):
            self.channel_layer.group_discard(self.group_name, self.channel_name)

    def send_notification(self, event):
        # Sends the notification message to the WebSocket.
        message = event["message"]
        print("message recieved", message)
        self.send(text_data=json.dumps({"message": message}))