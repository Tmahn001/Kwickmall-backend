from rest_framework import serializers, viewsets
from .models import Chat, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        chat = validated_data['chat']
        sender_id = validated_data['sender_id']
        if not chat.is_open:
            raise serializers.ValidationError("This chat is closed. You cannot send messages.")

        chat_buyer_id = chat.buyer_id
        chat_seller_id = chat.seller_id
        
        if sender_id != chat_buyer_id and sender_id != chat_seller_id:
            raise serializers.ValidationError("You are not allowed to send messages in this chat.")
        
        message = Message.objects.create(**validated_data)
        return message



class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    is_open = serializers.BooleanField(read_only=True)


    class Meta:
        model = Chat
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['is_open'] = True  # Add this line to set is_open to True
        chat = Chat.objects.create(**validated_data)
        return chat



