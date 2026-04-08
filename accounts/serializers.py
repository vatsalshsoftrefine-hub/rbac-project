from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    """
    Serializer is responsible for:
    1. Validating incoming data (username, password)
    2. Converting JSON → Python data (deserialization)
    3. Ensuring clean and safe input before DB operation

    WHY NOT DIRECTLY USE request.data?
    - request.data is raw (unsafe)
    - No validation (missing fields, wrong types)
    - No structure

    Serializer gives:
    - validation
    - clean data
    - reusable logic
    """

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)