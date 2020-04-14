from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
import json
import logging
from django.contrib.auth import get_user_model

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_channel_layer_group = self.room_id
        
        async_to_sync(self.channel_layer.group_add){
            self.room_channel_layer_group,
            self.channel_name
        }
        
        self.accept()
        
        messages = Message.objects.filter(room_id=self.room_id)
        
        for message in messages:
            self.send(text_data=json.dumps({
                'user_id': message.user.id,
                'user_name': message.user.username,
                'command': 'saved_message',
                'message': message.content,
            }))
            
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard){
            self.room_channel_layer_group,
            self.channel_name
        }
    
    def receive(self, text_data):
        User = get_user_model()
        
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_channel_layer_group = self.room_id
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user_name = text_data_json['user_name']
        
        # logger.error("message: " + message)
        
        message_object = Message.objects.create(
            user=User(pk=user_id),
            content=message,
            room=Room(pk=self.room_id)
        )
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_channel_layer_group,
            {
                'type': 'chat_message',
                'message': message,
                'user_name': user_name,
                'user_id': user_id,
            }
        )
    
    def chat_message(self, event):
        message = event['message']
        user_name = event['user_name']
        user_id = event['user_id']
        
        
        self.send(text_data=json.dumps({
            'command': 'new_message',
            'message': message,
            'user_name': user_name,
            'user_id': user_id,
        }))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    