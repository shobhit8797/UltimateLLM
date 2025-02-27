import json
import logging
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from ultimate_llm.utilities.resources import GlobalResources
from document_parser.utils import compute_file_hash
from llm_chat.rag import RagPipeline
from ultimate_llm.settings.base import MEDIA_ROOT
from ultimate_llm.utilities.schema import SupportedParsers

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
)

logger = logging.getLogger(__name__)

chat_history = {}

PREDEFINED_QUESTIONS = [
    ("Who is the insurer of this policy?", "Who is the insurance provider?"),
    (
        "List the insured members.",
        "List the insured persons.",
    ),
    ("What is the sum insured amount?", "What is the total sum insured?"),
    (
        "What is the room rent amount or category included in the policy?",
        "What is the room rent amount included in the policy?",
    ),
    (
        "What is the ICU room rent amount included in the policy?",
        "What is the ICU room rent amount included in the policy?",
    ),
    (
        "Does the policy include maternity coverage? If yes, what is the sum insured?",
        "Does the policy include maternity coverage? If yes, what is the sum insured? If you dont find any information, please give the ans no.",
    ),
    (
        "Is copay or co-payment opted? If yes, what is the copay or co-payment percentage?",
        "Does the policy have copay or co-payment? If yes, what is the co-payment percentage? Respond with 'Yes' followed by the percentage if applicable; otherwise, respond with 'No'.",
    ),
]
# PREDEFINED_QUESTIONS = [
#     {
#         "questions": ("Who is the insurer of this policy?", "Who is the insurance provider?"),
#         'pages': ((0, 1), (0, 5)),
#         "keywords": ["insurer", "insurance provider"]

#     }
# ]


def save_file(file, folder_name: str) -> tuple[Path, str]:
    file_storage = FileSystemStorage()
    saved_path = Path(file_storage.save(f"temp/{folder_name}/{file.name}", file))
    full_path = MEDIA_ROOT / saved_path
    return full_path, compute_file_hash(full_path)


def update_chat_history(policy_checksum: str, sender: str, message: str):
    chat_history.setdefault(policy_checksum, []).append(
        {"sender": sender, "text": message}
    )


def process_and_update_chat(question, policy_checksum, page_limit):
    _question = question[0]

    rag_pipeline = RagPipeline()

    answer = rag_pipeline.retrieval_pipeline(
        policy_checksum, _question, page_no_limit=page_limit
    )
    update_chat_history(policy_checksum, "user", _question)

    if "not available" in answer or "policy does not cover this" in answer:
        _question = question[1]
        answer = rag_pipeline.retrieval_pipeline(
            policy_checksum, _question, top_k=4, page_no_limit=3
        )

    update_chat_history(policy_checksum, "bot", answer)
    return answer


@csrf_exempt
def chat_view(request, policy_checksum=None):
    """Renders the chat interface."""
    return render(
        request,
        "chat.html",
        {
            "messages": chat_history,
            "policy_checksum": policy_checksum,
        },
    )


@csrf_exempt
def upload_policy(request):
    """Handles file upload and processing."""
    if request.method != "POST":
        return HttpResponseBadRequest("Unsupported request method")

    try:
        insurance_policy = request.FILES.get("insurance_policy")
        if not insurance_policy:
            return HttpResponseBadRequest("Please provide an insurance policy.")
        parser = SupportedParsers.PyPdf

        policy_path, policy_checksum = save_file(insurance_policy, "insurance_policies")
        RagPipeline().indexing_pipeline(policy_path, parser)

        update_chat_history(
            policy_checksum, "bot", f"Document Uploaded: {insurance_policy.name}"
        )
        return redirect("predefined_questions", policy_checksum=policy_checksum)

    except ValidationError as e:
        return HttpResponseBadRequest(f"File upload error: {e.message}")
    except Exception as e:
        logger.error(f"Error processing files: {e}: {e.__traceback__.tb_lineno}")
        return HttpResponseBadRequest("An error occurred while processing files.")


@csrf_exempt
def predefined_questions(request, policy_checksum):
    for index, question in enumerate(PREDEFINED_QUESTIONS):
        try:
            page_limit = 3 if index <= 2 else 12
            answer = process_and_update_chat(question, policy_checksum, page_limit)
        except Exception as e:
            logger.error(f"Error answering question '{question}': {e}")
            update_chat_history(
                policy_checksum, "bot", f"Error answering question: {question}"
            )

    return redirect("chat_view_checksum", policy_checksum=policy_checksum)


@csrf_exempt
def send_message(request, policy_checksum):
    """Handles user chat messages and responds."""
    if request.method != "POST":
        return HttpResponseBadRequest("Unsupported request method")

    user_question = request.POST.get("message")
    if not user_question:
        return HttpResponseBadRequest("Message field is required.")

    try:
        process_and_update_chat((user_question, user_question), policy_checksum, None)
        return redirect("chat_view_checksum", policy_checksum=policy_checksum)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return HttpResponseBadRequest(
            "An error occurred while processing your message."
        )


@csrf_exempt
def clear_chat(request, policy_checksum):
    """Clears the chat history."""
    chat_history[policy_checksum] = []
    return redirect("chat_view")


def generate_assistant_response(conversation):
    """
    Placeholder for LLM integration. In a real application, this would call an LLM API
    (e.g., OpenAI, Grok) with conversation history as context.
    """
    messages = conversation.messages.order_by("created_at").all()[
        -5:
    ]  # Last 5 messages for context
    prompt = ""
    for msg in messages:
        prompt += f"{'User' if msg.is_user else 'Assistant'}: {msg.text}\n"
    prompt += "Assistant: "
    # Dummy response for this example
    return "This is a response from the assistant based on the conversation."


class ConversationViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated 
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

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        print("conversation:", conversation)
        user_message_text = request.data.get("message")
        print("user_message_text:", user_message_text)

        # Validate input
        if not user_message_text:
            return Response(
                {"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save user's message
        user_message = Message.objects.create(
            conversation=conversation, text=user_message_text, is_user=True
        )
        user_message_data = MessageSerializer(user_message).data

        # Initialize the response generator
        generator = ResponseGenerator(conversation)

        def streaming_content():
            """
            Generator that streams JSON objects for the user message,
            assistant chunks, and completion signal.
            """
            # Step 1: Yield the user message
            yield json.dumps({"user_message": user_message_data}) + "\n"

            # Step 2: Yield assistant response chunks
            llm = GlobalResources().get_chat_llm()
            for chunk in llm.stream(user_message_data):
                yield json.dumps({"assistant_chunk": chunk}) + "\n"

            # Step 3: Save the assistant message after all chunks are streamed
            assistant_message = Message.objects.create(
                conversation=conversation,
                text=generator.full_response.strip(),
                is_user=False,
            )

            # Step 4: Yield completion signal
            yield json.dumps({"done": True}) + "\n"

        # Return streaming response
        response = StreamingHttpResponse(streaming_content(), content_type="text/plain")
        return response
