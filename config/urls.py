"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import ChatViewSet, MessageViewSet
from rest_framework import routers
from api.views import ChatViewSet, MessageViewSet, ChatMessageListView, CloseChatView, SellerChatMessageListView, SellerOpenChatListView, AdminChatMessageListView, AdminOpenChatListView, BuyerChatMessageListView, BuyerOpenChatListView, OpenChatCount
from django.conf import settings
from django.conf.urls.static import static
from api import consumers
from . import routing

router = routers.DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    *router.urls,
    path('ws/chat/<uuid:chat_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/', include(routing.websocket_urlpatterns)),
    path('chats/<uuid:chat_id>/close/', CloseChatView.as_view(), name='close-chat'),
    path('api/seller/<str:seller_id>/chats/', SellerOpenChatListView.as_view(), name='seller-open-chats'),
    path('api/buyer/<str:buyer_id>/chats/', BuyerOpenChatListView.as_view(), name='buyer-open-chats'),
    path('api/admin/chats/', AdminOpenChatListView.as_view(), name='admin-open-chats'),
    path('api/chats/<uuid:chat_id>/', ChatMessageListView.as_view(), name='chats'),
    path('api/seller/<str:seller_id>/chats/<uuid:chat_id>/messages/', SellerChatMessageListView.as_view(), name='seller-chat-messages'),
    path('api/buyer/<str:buyer_id>/chats/<uuid:chat_id>/messages/', BuyerChatMessageListView.as_view(), name='buyer-chat-messages'),
    path('api/admin/chats/<uuid:chat_id>/messages/', AdminChatMessageListView.as_view(), name='admin-chat-messages'),
    path('api/open-chat/', OpenChatCount.as_view(), name='open-unresolved-chat-count'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
