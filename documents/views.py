from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserModel
from .models import DocumentModel

# Create your views here.
import os

class UploadDocumentView(APIView):
    """
    Upload PDF and store metadata
    """

    def post(self, request):
        # Step 1: Get token
        token = request.auth

        if not token:
            return Response({"error": "No token"}, status=401)

        user_id = token.get("user_id")

        # Step 2: Get file
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # Step 3: Validate PDF
        if not file.name.endswith(".pdf"):
            return Response({"error": "Only PDF allowed"}, status=400)

        #  Step 4: Ensure media folder exists
        media_root = "/app/media"
        os.makedirs(media_root, exist_ok=True)

        # Step 5: Save file locally
        file_path = os.path.join(media_root, file.name)

        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Step 6: Save metadata
        doc = DocumentModel(
            user_id=user_id,
            file_name=file.name,
            file_url=file_path
        )
        doc.save()

        return Response({
            "message": "File uploaded successfully"
        })
    
class MyDocumentsView(APIView):
    """
    User can view their own documents
    """

    def get(self, request):
        # Step 1: Get token
        token = request.auth

        if not token:
            return Response({"error": "No token"}, status=401)

        # Step 2: Extract user_id
        user_id = token.get("user_id")

        # Step 3: Fetch documents
        documents = []

        for doc in DocumentModel.scan():
            if doc.user_id == user_id and doc.is_active:
                documents.append({
                    "document_id": doc.document_id,
                    "file_name": doc.file_name,
                    "file_url": doc.file_url
                })

        return Response(documents)