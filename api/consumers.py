import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        self.send(text_data=json.dumps({
            'message':"Connected to Socket ",
        }))

    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        color = text_data_json['color']
        print("message",message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'color':color
            }
        )

    def chat_message(self,event):
        message = event['message']
        color = event['color']
        print("chat_message",message)
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'color':color
        }))