import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserModel
from .serializers import RegisterSerializer
from .serializers import LoginSerializer


from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import UserModel



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
                password=make_password(data['password']),  # Hash the password
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
    
class LoginUser(APIView):
    """
    Handles user login.

    - We manually fetch user from DynamoDB
    - We manually verify password
    """

    def post(self, request):
        # Step 1: Validate request data
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            username = data['username']
            password = data['password']

            # Step 2: Find user in DynamoDB
            user = None

            for u in UserModel.scan():
                if u.username == username:
                    user = u
                    break

            # Step 3: Check if user exists
            if not user:
                return Response(
                    {"error": "User not found"},
                    status=404
                )

            # Step 4: Verify password
            if not check_password(password, user.password):
                return Response(
                    {"error": "Invalid password"},
                    status=400
                )

            # Step 5: Generate JWT tokens
            refresh = RefreshToken()
            refresh['user_id'] = user.user_id
            refresh['role'] = user.role
            return Response({
               "message": "Login successful",
               "tokens": {         
                   "refresh": str(refresh),
                   "access": str(refresh.access_token),               
                },
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "role": user.role
                }
})
        return Response(serializer.errors, status=400) 
    
class ProfileView(APIView):
    """
    Returns full profile of logged-in user using JWT
    """

    def get(self, request):
        """
        Step 1: Get token
        Step 2: Extract user_id
        Step 3: Fetch user from DynamoDB
        Step 4: Return user details
        """

        # Step 1: Extract token from request
        token = request.auth

        if not token:
            return Response(
                {"error": "Authentication token missing"},
                status=401
            )

        # Step 2: Extract user_id from token
        user_id = token.get("user_id")

        # Step 3: Fetch user from DynamoDB
        try:
            user = UserModel.get(user_id)
        except:
            return Response(
                {"error": "User not found"},
                status=404
            )

        # Step 4: Return user data
        return Response({
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "gender": user.gender,
            "role": user.role
        })