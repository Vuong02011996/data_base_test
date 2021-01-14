from mongoengine import StringField, DateTimeField, Document
from datetime import datetime


class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    name = StringField(required=True)

    created_at = DateTimeField(default=datetime.utcnow, required=True)

    meta = {"collection": "users"}
