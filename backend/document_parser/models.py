import hashlib

from django.core.exceptions import ValidationError
from django.db import models
from langchain_core.documents import Document

from document_parser.utils import compute_file_hash


class DocumentStore(models.Model):
    """
    Represents the uploaded document and its metadata.
    """

    title = models.CharField(max_length=255, help_text="Title or name of the document")
    upload_date = models.DateTimeField(
        auto_now_add=True, help_text="Date when the document was uploaded"
    )
    file_path = models.TextField()
    file_checksum = models.CharField(
        max_length=64, unique=True, help_text="Unique hash of the file content"
    )
    status = models.CharField(
        max_length=50,
        choices=[("parsed", "Parsed"), ("pending", "Pending"), ("failed", "Failed")],
        default="pending",
        help_text="Status of document parsing",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Compute hash before saving
        if not self.file_checksum:
            file_checksum = compute_file_hash(self.file_path)

        super().save(*args, **kwargs)


class ParsedElement(models.Model):
    """
    Represents individual parsed elements from the document.
    """

    ELEMENT_TYPE_CHOICES = [
        ("paragraph", "Paragraph"),
        ("table", "Table"),
        ("heading", "Heading"),
        ("list", "List"),
        ("image", "Image"),
        ("metadata", "Metadata"),
    ]

    element_id = models.CharField(max_length=33, default=hashlib.sha256().hexdigest())

    document = models.ForeignKey(
        DocumentStore,
        on_delete=models.CASCADE,
        related_name="parsed_elements",
        help_text="The document from which this element was parsed",
    )
    # element_type = models.CharField(
    #     max_length=50,
    #     choices=ELEMENT_TYPE_CHOICES,
    #     help_text="Type of the parsed element",
    # )
    content = models.TextField(
        help_text="The textual content of the parsed element, if applicable"
    )
    # order = models.PositiveIntegerField(
    #     help_text="Order of the element in the document"
    # )
    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Additional metadata associated with the element (e.g., table structure, image data)",
    )

    class Meta:
        # ordering = ["order"]
        verbose_name = "Parsed Element"
        verbose_name_plural = "Parsed Elements"

    def __str__(self):
        return f"{self.element_id}"

    def get_document(self) -> Document:
        return Document(
            page_content=self.content, metadata=self.metadata, id=self.element_id
        )


class DocumentMetadata(models.Model):
    document = models.OneToOneField(
        DocumentStore,
        on_delete=models.CASCADE,
        related_name="metadata",
        help_text="The document to which this metadata belongs",
    )
    key = models.CharField(max_length=255, help_text="Metadata key (e.g., 'Author')")
    value = models.TextField(help_text="Metadata value")

    def __str__(self):
        return f"{self.key}: {self.value}"
