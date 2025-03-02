import uuid
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


from users.models import User


class Role(models.TextChoices):
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
    role = models.CharField(max_length=1, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        role_name = dict(Role.choices).get(self.role, "Unknown")
        truncated_text = (self.text[:50] + "...") if len(self.text) > 50 else self.text
        return f"{role_name}: {truncated_text}"
