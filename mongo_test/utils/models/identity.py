from enum import Enum

from mongoengine import (
    StringField,
    DateTimeField,
    Document,
    LongField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    FloatField,
    IntField,
    LazyReferenceField,
    EnumField,
)
import datetime


class IdentityType(Enum):
    KNOWN = "known"
    UNKNOWN = "unknown"


class IdentityStatus(Enum):
    TRACKING = "tracking"
    UNTRACKING = "untracking"


class MatchingFace(EmbeddedDocument):
    face_id = LongField(required=True)
    url = StringField(required=True)


class ClusteringFace(EmbeddedDocument):
    object = LazyReferenceField("Object", required=True)
    face_id = LongField(required=True)
    url = StringField(required=True)
    head_pose = ListField(IntField(required=True), default=[])
    width = IntField(min_value=0, required=True)
    height = IntField(min_value=0, required=True)
    sharpness = FloatField(min_value=0, required=True)


class Identity(Document):
    process = LazyReferenceField("Process")
    name = StringField(required=True)
    card_number = StringField()

    type = EnumField(IdentityType, default=IdentityType.KNOWN, required=True)
    status = EnumField(IdentityStatus, default=IdentityStatus.TRACKING, required=True)
    matching_face_ids = ListField(EmbeddedDocumentField(MatchingFace))
    clustering_face_ids = ListField(ListField(EmbeddedDocumentField(ClusteringFace)))

    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)

    meta = {"collection": "identities"}
