from django.conf import settings
from django.shortcuts import render


def upload_pdf(request):
    if request.method == "POST":
        #         file = request.FILES["policy_document"]
        #         file_path = f"{settings.MEDIA_ROOT}/{file.name}"

        #         # Save the uploaded file to the media directory
        #         with open(file_path, "wb+") as destination:
        #             for chunk in file.chunks():
        #                 destination.write(chunk)

        #         pages = load_pdf(file_path)
        #         chunks = split_text(pages, 800, 200)
        #         documents = prepare_documents(chunks)

        #         # Do something with documents (e.g., save to database, pass to another view)

        return render(
            request, "document_parser/result.html"
        )  # , {"documents": documents})

    return render(request, "document_parser/upload.html")
