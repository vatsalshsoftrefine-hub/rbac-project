from .views import UploadDocumentView
from django.urls import path
from .views import MyDocumentsView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view()),
    path('my-documents/', MyDocumentsView.as_view()),
]