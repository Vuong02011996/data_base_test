from mongoengine import StringField, IntField, FloatField, Document, DateTimeField, LazyReferenceField, EmbeddedDocument, ListField, EmbeddedDocumentField
import datetime

from app.models.geometry import Polygon


class Regions(EmbeddedDocument):
    detecting_region = EmbeddedDocumentField(Polygon)
    tracking_region = EmbeddedDocumentField(Polygon)


class Config(EmbeddedDocument):
    detection_scale = FloatField(min=0, required=True)
    frame_drop = IntField(min=0, required=True)
    frame_step = IntField(min=0, required=True)
    frame_width = IntField(min=0, required=True)
    frame_height = IntField(min=0, required=True)

    max_pitch = IntField(required=True)
    max_roll = IntField(required=True)
    max_yaw = IntField(required=True)
    min_face_size = IntField(min=0, required=True)
    tracking_scale = FloatField(min=0, required=True)

    biometric_threshold = IntField(min=0, required=True)
    min_head_confidence = IntField(min=0, required=True)
    min_face_confidence = IntField(min=0, required=True)
    min_body_confidence = IntField(min=0, required=True)

    write_video_step = IntField(min=0, required=True)
    write_data_step = IntField(min=0, required=True)

    view_width = IntField(min=0, required=True)
    view_height = IntField(min=0, required=True)

    regions = ListField(EmbeddedDocumentField(Regions))


class Process(Document):
    camera = LazyReferenceField("Camera")
    user = LazyReferenceField("User", required=True)
    uuid = IntField(required=True)
    name = StringField(required=True)
    url = StringField()

    file_root = StringField(required=True)
    started_at = DateTimeField(required=True)
    config = EmbeddedDocumentField(Config, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)

    meta = {"collection": "processes"}
