from typing import Any, Literal, Optional

from langchain.schema import Document as BaseDocument


class Document(BaseDocument):
    """
    A document class extending the BaseDocument for flexible content handling.

    Attributes:
        content: Raw content of the document, of any type.
        source: Optional identifier for the document's source.
        channel: Optional display channel (e.g., "chat", "info", "index", "debug", "plot").
    """

    content: Any = None
    source: Optional[str] = None
    channel: Optional[Literal["chat", "info", "index", "debug", "plot"]] = None

    def __init__(self, content: Optional[Any] = None, *args, **kwargs):
        # If no content is provided, use alternate kwargs as content
        if content is None:
            content = kwargs.pop("text", None) or kwargs.pop("embedding", None)
            kwargs.setdefault("text", "<EMBEDDING>" if "embedding" in kwargs else "")
        elif isinstance(content, Document):
            # Copy attributes from another Document instance
            kwargs.update(content.dict())

        # Ensure content and text alignment
        kwargs["content"] = content
        kwargs.setdefault("text", str(content) if content else "")

        super().__init__(*args, **kwargs)

    def __bool__(self):
        return bool(self.content)

    @classmethod
    def example(cls) -> "Document":
        """Generate an example Document instance."""
        return cls(
            text="Sample text for the Document example.",
            metadata={"filename": "README.md", "category": "codebase"},
        )

    def __str__(self):
        return str(self.content)


from enum import Enum


class SupportedParsers(Enum):
    PyPdf = "pypdf"
    Unstructured = "unstructured"
    Marker = "marker"
