from mongoengine import (
    LazyReferenceField,
    IntField,
    ListField,
    FloatField,
    Document,
)


class Detection(Document):
    object = LazyReferenceField("Object", required=True)
    frame_index = IntField(required=True, min_value=0)

    head_bbox = ListField(FloatField(min_value=0, required=True), default=[])
    head_confidence = IntField(min_value=0)
    face_bbox = ListField(FloatField(min_value=0, required=True), default=[])
    face_confidence = IntField(min_value=0)
    body_bbox = ListField(FloatField(min_value=0, required=True), default=[])
    body_confidence = IntField(min_value=0)
    head_pose = ListField(IntField(required=True), default=[])

    meta = {"collection": "detections"}
