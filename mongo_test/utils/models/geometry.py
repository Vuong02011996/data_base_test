from mongoengine import (
    EmbeddedDocument,
    StringField,
    ListField,
    FloatField,
)


class Polygon(EmbeddedDocument):
    type = StringField(required=True)
    coordinates = ListField(ListField(ListField(FloatField(min_value=0, required=True), required=True), required=True), required=True)
