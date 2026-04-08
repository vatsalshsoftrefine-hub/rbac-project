from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class UserModel(Model):
    """
    This model represents a user in DynamoDB.

    """

    class Meta:
        table_name = "users"
        region = "us-west-2"
        host = "http://dynamodb:8000"

    # Primary key (like id in SQL)
    user_id = UnicodeAttribute(hash_key=True)

    # User fields
    username = UnicodeAttribute()
    email = UnicodeAttribute()
    password = UnicodeAttribute()
    phone = UnicodeAttribute()
    role = UnicodeAttribute()
    gender = UnicodeAttribute()