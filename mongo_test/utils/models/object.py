from mongoengine import (
    Document,
    LongField,
    IntField,
    DateTimeField,
    LazyReferenceField,
    StringField,
    ListField,
    EmbeddedDocument,
    FloatField,
    EmbeddedDocumentField,
    BooleanField,
)
import datetime


class Face(EmbeddedDocument):
    face_id = LongField(required=True)
    url = StringField()
    head_pose = ListField(IntField(required=True), default=[])
    width = IntField(min_value=0, required=True)
    height = IntField(min_value=0, required=True)
    sharpness = FloatField(min_value=0, required=True)


class Body(EmbeddedDocument):
    body_id = LongField(required=True)
    width = IntField(min_value=0, required=True)
    height = IntField(min_value=0, required=True)
    sharpness = FloatField(min_value=0, required=True)


class Object(Document):
    process = LazyReferenceField("Process", required=True)
    identity = LazyReferenceField("Identity")

    uuid = LongField(unique=True, required=True, min_value=0)
    track_id = IntField(required=True, min_value=0)
    avatars = ListField(StringField(required=True), required=True)
    confidence_rate = IntField()
    similarity_distance = FloatField()
    age = IntField(min_value=0)
    gender = StringField()
    from_frame = IntField(required=True, min_value=0)
    to_frame = IntField(min_value=0)
    from_time = DateTimeField()
    to_time = DateTimeField()

    face_ids = ListField(ListField(EmbeddedDocumentField(Face)), default={})
    body_ids = ListField(EmbeddedDocumentField(Body), default=[])
    have_new_face = BooleanField(default=False, required=True)
    have_new_body = BooleanField(default=False, required=True)

    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)

    meta = {"collection": "objects"}
