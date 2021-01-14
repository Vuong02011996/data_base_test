from mongoengine import (
    DateTimeField,
    Document,
    LazyReferenceField,
)
from datetime import datetime


class Cluster(Document):
    identity = LazyReferenceField("Identity")
    created_at = DateTimeField(default=datetime.utcnow, required=True)

    meta = {"collection": "clusters"}
