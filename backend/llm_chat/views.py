import json
import logging

from django.http import StreamingHttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.generics import RetrieveAPIView
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

    def retrieve(self, request, pk=None):
        """Retrieve a specific conversation with its messages."""
        try:
            conversation = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """Create a new conversation and handle message streaming."""
        user_message_text = request.data.get("message")
        conversation_id = request.data.get("conversation_id")

        # Validate input
        if not user_message_text:
            return Response(
                {"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not conversation_id:
            conversation = Conversation.objects.create(user=request.user)
            print("Creating Conversation")
        else:
            try:
                conversation = self.get_queryset().get(pk=conversation_id)
            except Conversation.DoesNotExist:
                return Response(
                    {"error": "Conversation not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Create user message
        user_message = Message.objects.create(
            conversation=conversation, text=user_message_text, sender=Sender.USER
        )
        user_message_data = MessageSerializer(user_message).data

        def streaming_content():
            """
            Generator that streams JSON objects for the user message,
            assistant chunks, and completion signal.
            """
            try:
                yield json.dumps(user_message_data) + "\n"

                messages = [("system", ""), ("user", user_message_data["text"])]
                llm = GlobalResources().get_chat_llm()

                ai_message = Message.objects.create(
                    conversation=conversation,
                    text="",
                    sender=Sender.ASSISTANT,
                )

                full_response = ""
                for chunk in llm.stream(messages):
                    full_response += chunk.content
                    if chunk.response_metadata.get("finish_reason") == "stop":
                        break

                    yield json.dumps(
                        {
                            "id": str(ai_message.id),
                            "conversation": str(conversation.id),
                            "text": chunk.content,  # Fixed: Use chunk.content instead of chunk.text()
                            "sender": "A",  # Fixed: Use string "A" instead of Sender.ASSISTANT
                            "created_at": ai_message.created_at.strftime(
                                format="%Y-%m-%dT%H:%M:%SZ"
                            ),
                        }
                    ) + "\n"

                ai_message.text = full_response.strip()
                ai_message.save()

                yield json.dumps({"text": "DONE"}) + "\n"

            except Exception as e:
                logger.error(f"Error in streaming_content: {str(e)}")
                yield json.dumps({"error": f"An error occurred: {str(e)}"}) + "\n"

        return StreamingHttpResponse(
            streaming_content(), content_type="text/event-stream"
        )

#     def create(self, request):
#         """Create a new conversation and handle message streaming."""
#         user_message_text = request.data.get("message")
#         conversation_id = request.data.get("conversation_id")

#         # Validate input
#         if not user_message_text:
#             return Response(
#                 {"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         if not conversation_id:
#             conversation = Conversation.objects.create(user=request.user)
#             print("Creating Conversation")
#         else:
#             conversation = self.get_object()

#         # Create user message
#         user_message = Message.objects.create(
#             conversation=conversation, text=user_message_text, sender=Sender.USER
#         )
#         user_message_data = MessageSerializer(user_message).data

#         def streaming_content():
#             """
#             Generator that streams JSON objects for the user message,
#             assistant chunks, and completion signal.
#             """
#             try:
#                 yield json.dumps(user_message_data) + "\n"

#                 messages = [("system", ""), ("user", user_message_data["text"])]
#                 llm = GlobalResources().get_chat_llm()

#                 ai_message = Message.objects.create(
#                     conversation=conversation,
#                     text="",
#                     sender=Sender.ASSISTANT,
#                 )

#                 full_response = ""
#                 for chunk in llm.stream(messages):
#                     full_response += chunk.content
#                     if chunk.response_metadata.get("finish_reason") == "stop":
#                         break

#                     yield json.dumps(
#                         {
#                             "id": str(ai_message.id),
#                             "conversation": str(conversation.id),
#                             "text": chunk.text(),
#                             "sender": Sender.ASSISTANT,
#                             "created_at": ai_message.created_at.strftime(
#                                 format="%Y-%m-%dT%H:%M:%SZ"
#                             ),
#                         }
#                     ) + "\n"

#                 ai_message.text = full_response.strip()
#                 ai_message.save()

#                 yield json.dumps({"text": "DONE"}) + "\n"

#             except Exception as e:
#                 logger.error(f"Error in streaming_content: {str(e)}")
#                 yield json.dumps({"error": f"An error occurred: {str(e)}"}) + "\n"

#         return StreamingHttpResponse(
#             streaming_content(), content_type="text/event-stream"
#         )


# class MessageViewSet(RetrieveAPIView):
#     """Retrieve a single conversation's messages."""

#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationDetailSerializer
