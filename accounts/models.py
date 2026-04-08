from django.db import models

# Create your models here.
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class UserModel(Model):
    class Meta:
        table_name = "users"
        region = "us-west-2"
        host = "http://dynamodb:8000"   # 🔥 IMPORTANT (docker service name)

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    password = UnicodeAttribute()
    role = UnicodeAttribute()