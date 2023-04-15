import json 
from datetime import datetime 
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer 
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync 

from projects.models import Project
from live.models import ChatMessage, Notification 

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

        message_exists = ChatMessage.objects.filter(
            user = self.scope["user"], 
            project = self.project, 
            message = message 
        ).exists()

        if not message_exists:
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

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'notifications', self.channel_name
        )
        await self.accept()
        notifications = await self.get_notifications()
        for i in notifications: 
            date = i["date"].strftime('%Y-%m-%d %H:%M')
            await self.send(text_data = json.dumps({
                "message": i["message"], 
                "date": date,
                "project_id": i["project_id"]
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'notifications', self.channel_name 
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        project = text_data_json["project"]
        user = text_data_json["user"]
        await self.channel_layer.group_send(
            'notifications', 
            {
                'type': 'send_notifications', 
                'message': message,
                'project': project, 
                'user': user,  
            }
        )
    
    async def send_notification(self, event):
        message = event["message"]
        now = datetime.now()
        await self.send(text_data=json.dumps({
            'message': message, 
            'date': now.isoformat(),
        }))

    @database_sync_to_async
    def get_notifications(self):
        return list(Notification.objects.exclude(user = self.scope["user"]).values().order_by("-id"))

    @database_sync_to_async
    def create_notification(self, message, project, user):
        return Notification.objects.create(
            message = message, 
            project = project, 
            user = user, 
        )

