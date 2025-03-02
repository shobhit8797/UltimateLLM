import json
import logging
from rest_framework import permissions

from ultimate_llm.utilities.resources import GlobalResources
import json
import logging
from ultimate_llm.utilities.resources import GlobalResources
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse 
from .models import Conversation, Message
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, Message
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
        print("I am here ")
        user_message_text = request.data.get("message")

        # Validate input
        if not user_message_text:
            return Response(
                {"error": "Text is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create conversation
        if not pk:
            conversation = Conversation.objects.create(user=request.user)
        else:
            conversation = self.get_object()
        
        # Create user message
        user_message = Message.objects.create(
            conversation=conversation, 
            text=user_message_text, 
            is_user=True
        )
        user_message_data = MessageSerializer(user_message).data
        print(":user_message_data:", user_message_data)


        def streaming_content():
            """
            Generator that streams JSON objects for the user message,
            assistant chunks, and completion signal.
            """
            try:
                yield json.dumps({
                    "conversation_id": conversation.id, 
                    "user_message": user_message_data
                }) + "\n"

                messages = [("system","",),("user", user_message_data["text"])]
                llm = GlobalResources().get_chat_llm()
                print("user_message_data:", user_message_data["text"])
                print("llm:", llm)
                print("llm:", llm.stream(messages))
                

                # full_response = ""
                # for chunk in llm.stream(messages):  # Using text field specifically
                #     print("chunk.content:", chunk.content)
                #     full_response += chunk.content
                for chunk in llm.stream(messages):
                    print(chunk.text(), end="")
                    yield json.dumps({"assistant_chunk": chunk.text()}) + "\n"

                # Save the assistant message after all chunks are streamed
                # assistant_message = Message.objects.create(
                #     conversation=conversation,
                #     text=full_response.strip(),
                #     is_user=False,
                # )

                # Yield completion signal
                yield json.dumps({"done": True}) + "\n"
            
            except Exception as e:
                logger.error(f"Error in streaming_content: {str(e)}")
                yield json.dumps({
                    "error": f"An error occurred: {str(e)}"
                }) + "\n"

        # Return streaming response
        return StreamingHttpResponse(
            streaming_content(), 
            content_type="text/event-stream"  # More appropriate for streaming
        )