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


# View to retrieve all open chats for a particular seller
class SellerOpenChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Chat.objects.filter(seller_id=seller_id, is_open=True)

# View to retrieve all open chats for a particular buyer
class BuyerOpenChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        buyer_id = self.kwargs['buyer_id']
        return Chat.objects.filter(buyer_id=buyer_id, is_open=True)

# View to retrieve all open chats for admin
class AdminOpenChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(is_open=True)

# View to retrieve all messages of a seller in a particular chat
class SellerChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id, sender_id=seller_id)

# View to retrieve all messages of a buyer in a particular chat
class BuyerChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        buyer_id = self.kwargs['buyer_id']
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id, sender_id=buyer_id)

# View to retrieve all messages in a particular chat for admin
class AdminChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id, sender_id=1)

class CloseChatView(APIView):
    def put(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

        chat.close_chat()
        return Response({'message': 'Chat closed successfully'})