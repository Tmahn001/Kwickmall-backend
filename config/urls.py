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
from api.views import ChatViewSet, MessageViewSet, CloseChatView

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    *router.urls,
    path('chats/<uuid:chat_id>/close/', CloseChatView.as_view(), name='close-chat'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
