from datetime import datetime
from enum import Enum

from mongoengine import (
    EnumField,
    Document,
    LazyReferenceField,
    DateTimeField,
)


class ClusterType(Enum):
    FACE = "face"
    BODY = "body"


class ClusterElement(Document):
    cluster = LazyReferenceField("Cluster", required=True)
    object = LazyReferenceField("Object", required=True)
    ref_object = LazyReferenceField("Object")
    type = EnumField(ClusterType, default=ClusterType.FACE, required=True)

    created_at = DateTimeField(default=datetime.utcnow, required=True)

    meta = {"collection": "cluster_elements"}
