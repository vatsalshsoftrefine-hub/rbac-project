from .views import UploadDocumentView
from django.urls import path
from .views import MyDocumentsView
from .views import DeleteDocumentView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view()),
    path('my-documents/', MyDocumentsView.as_view()),
    path('delete/<str:document_id>/', DeleteDocumentView.as_view()),
]