import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserModel
from .serializers import RegisterSerializer


class RegisterUser(APIView):
    """
    This API handles user registration.

    Responsibilities:
    - Accept request data
    - Validate input using serializer
    - Create user in DynamoDB
    - Return appropriate response
    """

    def post(self, request):
        # Step 1: Pass incoming request data to serializer
        serializer = RegisterSerializer(data=request.data)

        # Step 2: Validate the data
        if serializer.is_valid():
            """
            serializer.is_valid() checks:
            - Required fields are present
            - Data types are correct
            - Custom validations (like role, password length)
            """

            data = serializer.validated_data
            """
            validated_data contains:
            - Cleaned data
            - Safe to use for database operations
            """

            # Step 3: Create user object for DynamoDB
            user = UserModel(
                user_id=str(uuid.uuid4()),   # unique identifier for user
                username=data['username'],
                email=data['email'],
                password=data['password'],   # plain for now, will hash later
                phone=data['phone'],
                gender=data['gender'],

                # Important security rule:
                # Even if user sends role=admin, we override it
                role="user"
            )

            # Step 4: Save user to DynamoDB
            user.save()

            # Step 5: Return success response
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        # Step 6: Return validation errors if any
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )