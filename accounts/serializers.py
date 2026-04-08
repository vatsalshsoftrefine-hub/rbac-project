from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """
    This serializer handles:
    1. Input validation
    2. Data cleaning
    3. Structure enforcement

    WHY NOT ModelSerializer?
    - We are using PynamoDB (NoSQL)
    - No Django ORM model
    - So we use basic Serializer instead
    """

    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)
    phone = serializers.CharField(max_length=15)
    role = serializers.CharField()
    gender = serializers.CharField()

    #  Validate role 
    def validate_role(self, value):
        """
        Ensures only valid roles are accepted
        """
        allowed_roles = ['admin', 'user']

        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid role selected")

        return value

    #  Extra validation (if needed)
    def validate(self, data):
        """
        Cross-field validation (if needed)
        Example: password strength, phone format, etc.
        """
        if len(data['password']) < 3:
            raise serializers.ValidationError("Password too short")

        return data