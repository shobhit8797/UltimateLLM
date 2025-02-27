from django.db import models

from users.models import User


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField()
    is_user = (
        models.BooleanField()
    )  # True for user messages, False for assistant messages
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'User' if self.is_user else 'Assistant'}: {self.text[:50]} {"..." if len(self.text) > 50 else None}"
