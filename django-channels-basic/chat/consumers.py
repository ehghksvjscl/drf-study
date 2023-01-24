from channels.layers import get_channel_layer
from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

class ChatConsumer(JsonWebsocketConsumer):
    SQUARER_GROUP_NAME = "square"
    groups = [SQUARER_GROUP_NAME]

    def recevie_json(self, content, **kwargs):
        _type = [content['type']]

        if _type == "chat.message":
            message = content['message']
            async_to_sync(self.channel_layer.group_send)(
                self.SQUARER_GROUP_NAME,
                {
                    "type": "chat.message",
                    "message": message
                }
            )
        else:
            print(f"Invalid message type: {_type}")

    def chat_message(self, message_dict):
        self.send_json({
            "type": "chat.message",
            "message": message_dict['message']
        })