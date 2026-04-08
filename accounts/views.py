from django.shortcuts import render
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserModel
from .serializers import RegisterSerializer


class RegisterUser(APIView):
    """
    APIView handles HTTP requests (POST, GET, etc.)

    This class handles:
    - Receiving request
    - Validating input
    - Creating user in DynamoDB
    - Sending response
    """

    def post(self, request):
        """
        POST request = user registration

        request.data contains incoming JSON
        """

        # Step 1: Validate data using serializer
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            """
            is_valid() checks:
            - required fields present?
            - correct data types?
            """

            data = serializer.validated_data
            """
            validated_data = clean, safe, structured data
            """

            # Step 2: Create user object
            user = UserModel(
                user_id=str(uuid.uuid4()),   # unique ID
                username=data['username'],
                password=data['password'],  
                role="user"   # 🔥 force role (security)
            )

            # Step 3: Save to DynamoDB
            user.save()

            # Step 4: Send success response
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        # Step 5: If validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)