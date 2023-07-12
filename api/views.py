from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Chat, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer, MessageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class CloseChatView(APIView):
    def put(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

        chat.close_chat()
        return Response({'message': 'Chat closed successfully'})