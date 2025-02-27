import multiprocessing
from abc import ABC, ABCMeta, abstractmethod
from threading import Lock
from typing import Any


class SingletonMeta(ABCMeta):
    """
    A metaclass for Singleton pattern. Ensures only one instance per class.
    """

    _instances = {}
    _lock = Lock()  # Ensure thread safety during instance creation

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
                cls.model_id = kwargs.get("model_id")
                cls.pipeline_kwargs = kwargs.get("pipeline_kwargs")
                cls.task = kwargs.get("task")
        return cls._instances[cls]


class BaseLLM(ABC):
    """
    Base class for all LLM implementations. Ensures only one instance per LLM type.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs): ...

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the LLM model. Must be implemented by subclasses.
        """
        pass

    # @abstractmethod
    # def run(self, input_text: Any, **kwargs) -> Any:
    #     """
    #     Perform chat/invoke functionality. Must be implemented by subclasses.
    #     """
    #     pass

    def _multiprocess_chat(self, input_text: Any) -> Any:
        """
        Wrapper function for multiprocessing-safe chat execution.
        """
        return self.run(input_text)

    def invoke(self, input_text: Any) -> Any:
        """
        Execute the chat function in a multiprocessing-safe manner.
        """
        with multiprocessing.Pool(1) as pool:
            result = pool.apply(self._multiprocess_chat, (input_text,))
        return result
