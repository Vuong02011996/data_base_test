from mongoengine import (
    StringField,
    DateTimeField,
    Document,
)
import datetime


class Camera(Document):
    name = StringField(required=True)
    url = StringField(required=True)

    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)

    meta = {"collection": "cameras"}
