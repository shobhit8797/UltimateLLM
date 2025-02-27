from django.urls import path

from . import views

urlpatterns: list = [path("index-files", views.IndexFile.as_view(), name="index_files")]
