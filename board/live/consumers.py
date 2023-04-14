import json 
from channels.generic.websocket import WebsocketConsumer 
from asgiref.sync import async_to_sync 

from projects.models import Project
from live.models import ChatMessage 

##### 

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["project_id"]
        self.room_group_name = "chat_%s" % self.room_name 
        self.project = Project.objects.get(id = self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name 
        )

        self.accept()

        messages = ChatMessage.objects.filter(project__id = self.room_name).order_by("date")
        for message in messages: 
            self.send(text_data=json.dumps({
                "message": message.message, 
                "user": message.user.username, 
                "date": message.date.isoformat(), 
            }))
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        ) 

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        new_message = ChatMessage.objects.create(
            user = self.scope["user"], 
            project = self.project, 
            message = message
        )

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": new_message.message, 
            "user": new_message.user.username, 
            "date": new_message.date.isoformat(),
        }))
