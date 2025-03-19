from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(source="conversation.id", read_only=True)
    timestamp = serializers.DateTimeField(
        source="created_at", format="%Y-%m-%dT%H:%M:%SZ", read_only=True
    )

    class Meta:
        model = Message
        fields = ["id", "conversation_id", "text", "sender", "timestamp"]


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "title", "messages", "created_at"]
