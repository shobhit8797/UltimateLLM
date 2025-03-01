from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from oauth2_provider.models import get_application_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views import TokenView
from rest_framework import status

class SignupView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to register


class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate credentials
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Get your OAuth application
        Application = get_application_model()
        try:
            app = Application.objects.get(
                client_id="10dkrsTt5NKwoFsxw6UoqgTsj4693S2lfW7bkSqU"
            )
        except Application.DoesNotExist:
            return Response(
                {"error": "OAuth application not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Simulate token request
        token_request_data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": app.client_id,
            "client_secret": "mysecret123",  # Replace with your actual client_secret
        }
        token_view = TokenView.as_view()
        token_response = token_view(
            request._request.__class__(method="POST", body=token_request_data)
        )

        if token_response.status_code == 200:
            return Response(token_response.data)
        return Response(token_response.data, status=token_response.status_code)
