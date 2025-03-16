import json
import logging

from django.http import StreamingHttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ultimate_llm.utilities.resources import GlobalResources

from .models import Conversation, Message, Sender
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
)

logger = logging.getLogger(__name__)


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Conversation.objects.all()

    def get_queryset(self):
        """Filter conversations to the authenticated user."""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == "list":
            return ConversationListSerializer
        return ConversationDetailSerializer

    def perform_create(self, serializer):
        """Assign the conversation to the authenticated user."""
        serializer.save(user=self.request.user)

    # @action(detail=True, methods=["post"])
    def create(self, request, pk=None):
        user_message_text = request.data.get("message")

        # Validate input
        if not user_message_text:
            return Response(
                {"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create conversation
        if not pk:
            conversation = Conversation.objects.create(user=request.user)
        else:
            conversation = self.get_object()

        # Create user message
        user_message = Message.objects.create(
            conversation=conversation, text=user_message_text, sender=Sender.USER
        )
        user_message_data = MessageSerializer(user_message).data
        print(":user_message_data:", user_message_data)

        def streaming_content():
            """
            Generator that streams JSON objects for the user message,
            assistant chunks, and completion signal.
            """
            try:
                yield json.dumps(user_message_data) + "\n"

                messages = [
                    (
                        "system",
                        "",
                    ),
                    ("user", user_message_data["text"]),
                ]
                llm = GlobalResources().get_chat_llm()

                ai_message = Message.objects.create(
                    conversation=conversation,
                    text="",
                    sender=Sender.ASSISTANT,
                )

                full_response = ""
                for chunk in llm.stream(messages):
                    full_response += chunk.content
                    print("*"*50)
                    print("chunk.text():", chunk.text())
                    print("chunk.content:", chunk.content)
                    print("response_metadata:", chunk.response_metadata)
                    print("*"*50)

                    if (chunk.response_metadata.get("finish_reason") == 'stop'):
                        break
                    
                    yield json.dumps(
                        {
                            "id": str(ai_message.id),
                            "conversation": str(conversation.id),
                            "text": chunk.text(),
                            "sender": Sender.ASSISTANT,
                            "created_at": ai_message.created_at.strftime(
                                format="%Y-%m-%dT%H:%M:%SZ"
                            ),
                        }
                    ) + "\n"

                ai_message.text = full_response.strip()
                ai_message.save()

                yield json.dumps({"text": "DONE"}) + "\n"

            except Exception as e:
                logger.error(
                    f"Error in streaming_content: {str(e)}: {e.__traceback__.tb_lineno}"
                )
                yield json.dumps({"error": f"An error occurred: {str(e)}"}) + "\n"

        return StreamingHttpResponse(
            streaming_content(), content_type="text/event-stream"
        )
