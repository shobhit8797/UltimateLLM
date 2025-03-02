from django.contrib.auth import authenticate
from oauth2_provider.models import get_application_model
from oauth2_provider.views import TokenView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate credentials
        username = request.data.get("email")
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
            "client_id": "10dkrsTt5NKwoFsxw6UoqgTsj4693S2lfW7bkSqU",
            "client_secret": "tsOxiH7SsvYYlQSLj5gbwMcuFbmniIBmNhbTJ4qP2lG26jfE0S8voIsGFObYbqZsrzvvBlD4zZDHuZSBc1wR4OI318legZAAvyYb86wCrillyZf9oTjjdTq11dpvtedJ",
        }

        request.build_absolute_uri
        factory = RequestFactory()
        token_request = factory.post(
            "/oauth/token/",  # The endpoint doesn't matter here; TokenView will process the data
            data=token_request_data,
            content_type="application/x-www-form-urlencoded",
        )

        # Call the TokenView with the simulated request
        token_view = TokenView.as_view()
        token_response = token_view(token_request)

        if token_response.status_code == 200:
            return Response(token_response.data)
        return Response(token_response.data, status=token_response.status_code)
