from mongoengine import (
    StringField,
    LazyReferenceField,
    Document,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
)
import datetime


class Threads(EmbeddedDocument):
    object_id = StringField()
    status = StringField()


class Logger(Document):
    process_id = LazyReferenceField("Process", required=True)
    data = EmbeddedDocumentField(Threads)

    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)

    meta = {"collection": "loggers"}
