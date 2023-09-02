from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Chat, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



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
'''class SellerChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id, sender_id=seller_id)'''
class SellerChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        seller_id = self.kwargs['seller_id']
        chat_id = self.kwargs['chat_id']
        
        seller_messages = queryset.filter(sender_id=seller_id)
        buyer_messages = queryset.exclude(sender_id=seller_id).exclude(sender_id=1)  # Exclude seller and admin messages
        admin_messages = queryset.filter(sender_id=1)

        data = {
            'seller_messages': self.get_serializer(seller_messages, many=True).data,
            'buyer_messages': self.get_serializer(buyer_messages, many=True).data,
            'admin_messages': self.get_serializer(admin_messages, many=True).data,
        }

        return Response(data)

# View to retrieve all messages of a buyer in a particular chat
class BuyerChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        buyer_id = self.kwargs['buyer_id']
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        buyer_id = self.kwargs['buyer_id']
        chat_id = self.kwargs['chat_id']
        
        buyer_messages = queryset.filter(sender_id=buyer_id)
        seller_messages = queryset.exclude(sender_id=buyer_id).exclude(sender_id=1)  # Exclude buyer and admin messages
        admin_messages = queryset.filter(sender_id=1)

        data = {
            'buyer_messages': self.get_serializer(buyer_messages, many=True).data,
            'seller_messages': self.get_serializer(seller_messages, many=True).data,
            'admin_messages': self.get_serializer(admin_messages, many=True).data,
        }

        return Response(data)

# View to retrieve all messages in a particular chat for admin
class AdminChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        chat_id = self.kwargs['chat_id']
        
        admin_messages = queryset.filter(sender_id=1)
        buyer_messages = queryset.exclude(sender_id=1).exclude(sender_id=chat.seller_id)  # Exclude admin and seller messages
        seller_messages = queryset.exclude(sender_id=1).exclude(sender_id=chat.buyer_id)  # Exclude admin and buyer messages

        data = {
            'admin_messages': self.get_serializer(admin_messages, many=True).data,
            'buyer_messages': self.get_serializer(buyer_messages, many=True).data,
            'seller_messages': self.get_serializer(seller_messages, many=True).data,
        }

        return Response(data)

# View to retrieve all messages in a particular chat
class ChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id).order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)

        messages = []
        for message in queryset:
            if message.sender_id == chat.seller_id:
                role = 'seller'
            elif message.sender_id == chat.buyer_id:
                role = 'buyer'
            else:
                role = 'admin'
            
            messages.append({
                'id': message.id,
                'role': role,
                'content': message.content,
                'attachment': message.attachment.url if message.attachment else None,
                'created_at': message.created_at,
            })

        return Response(messages)


class CloseChatView(APIView):
    def put(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

        chat.close_chat()
        return Response({'message': 'Chat closed successfully'})

class OpenChatCount(generics.ListAPIView):
    def get(self, request):
        open_unresolved_chat_count = Chat.objects.filter(is_open=True).count()
        return JsonResponse({'count': open_unresolved_chat_count})