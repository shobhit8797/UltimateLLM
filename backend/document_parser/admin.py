from django.contrib import admin

from document_parser.models import DocumentMetadata, DocumentStore, ParsedElement


@admin.register(DocumentStore)
class DocumentStoreAdmin(admin.ModelAdmin):
    list_display = ("title", "upload_date", "status")
    list_filter = ("status", "upload_date")
    search_fields = ("title", "file_checksum")
    readonly_fields = ("file_checksum", "upload_date")
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "file_path", "file_checksum", "status"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("upload_date",),
            },
        ),
    )


@admin.register(ParsedElement)
class ParsedElementAdmin(admin.ModelAdmin):
    list_display = ("element_id", "document", "content")
    list_filter = ("document",)
    search_fields = ("element_id", "content")
    fieldsets = (
        (
            None,
            {
                "fields": ("document", "content", "metadata"),
            },
        ),
    )


@admin.register(DocumentMetadata)
class DocumentMetadataAdmin(admin.ModelAdmin):
    list_display = ("document", "key", "value")
    list_filter = ("key",)
    search_fields = ("key", "value")
    fieldsets = (
        (
            None,
            {
                "fields": ("document", "key", "value"),
            },
        ),
    )
