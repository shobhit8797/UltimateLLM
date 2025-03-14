import uuid
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Sender(models.TextChoices):
    ASSISTANT = "A", _("Assistant")
    SYSTEM = "S", _("System")
    USER = "U", _("User")


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField()
    sender = models.CharField(max_length=1, choices=Sender.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        sender_name = dict(Sender.choices).get(self.sender, "Unknown")
        truncated_text = (
            sender_name(self.text[:50] + "...") if len(self.text) > 50 else self.text
        )
        return f"{sender_name}: {truncated_text}"
