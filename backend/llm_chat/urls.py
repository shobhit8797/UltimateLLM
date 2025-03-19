from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("conversations", views.ConversationViewSet)

urlpatterns: list = [
    path("", include(router.urls)),
    # path(
    #     "conversations/<int:pk>/",
    #     views.MessageViewSet.as_view(),
    #     name="conversation_message",
    # ),
]
