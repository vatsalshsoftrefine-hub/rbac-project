from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # DO NOT fetch Django user
        return None
    