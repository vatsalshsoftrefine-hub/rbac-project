from django.db import models
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
import uuid

# Create your models here.
class DocumentModel(Model):
    """
    DynamoDB model for storing document metadata
    """

    class Meta:
        table_name = "documents"
        host = "http://dynamodb-local:8000"
        region = "us-west-2"

    document_id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    user_id = UnicodeAttribute()
    file_name = UnicodeAttribute()
    file_url = UnicodeAttribute()
    is_active = BooleanAttribute(default=True)
