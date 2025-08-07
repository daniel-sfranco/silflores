import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Cart
from users.models import CustomUser
from asgiref.sync import sync_to_async


class Order(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"Usuário conectado ao chat {self.room_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Usuário desconectado do chat {self.room_name}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        messageProcessed = ":".join(message.split(":")[1:])
        senderUsername = message.split(":")[0]
        cartUser = self.room_name.split("-")[0]
        cart = await sync_to_async(Cart.objects.get)(user__username=cartUser)
        sender = await sync_to_async(CustomUser.objects.get)(username=senderUsername)
        messageObject = await sync_to_async(Message.objects.create)(content=messageProcessed, cart=cart, sender=sender)  # noqa: F841
        await self.send(text_data=json.dumps({'message': message}))
