from django.urls import path
from .views import UploadDocumentView, MyDocumentsView, DeleteDocumentView, DisableDocumentView, AllDocumentsView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view()),
    path('my-documents/', MyDocumentsView.as_view()),
    path('delete/<str:document_id>/', DeleteDocumentView.as_view()),
    path('disable/<str:document_id>/', DisableDocumentView.as_view()),
    path('all/', AllDocumentsView.as_view()),
]