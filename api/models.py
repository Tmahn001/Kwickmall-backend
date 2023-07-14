from django.db import models

# Create your models here.
import uuid
from django.db import models

class Chat(models.Model):
    issue = models.CharField(max_length=255, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer_id = models.CharField(max_length=255)
    seller_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)
    
    def close_chat(self):
        self.is_open = False
        self.save()

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender_id = models.CharField(max_length=255)
    content = models.TextField()
    attachment = models.FileField(blank=True, upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)


