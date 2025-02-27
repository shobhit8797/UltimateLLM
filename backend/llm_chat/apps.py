from django.apps import AppConfig

from ultimate_llm.utilities.resources import GlobalResources


class LlmChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "llm_chat"

    # def ready(self):
    #     GlobalResources.get_docstore()
    #     GlobalResources.get_embedding()
    #     GlobalResources.get_vectorstore()
    #     GlobalResources.get_chat_llm()
