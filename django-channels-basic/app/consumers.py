import json

from channels.generic.websocket import WebsocketConsumer

class EchoConsumer(WebsocketConsumer):

    def receive(self, text_data=None, bytes_data=None):
        obj = json.loads(text_data)
        result = json.dumps({
            'message': obj['message'],
            'sender': obj['sender'],
        })

        self.send(result)