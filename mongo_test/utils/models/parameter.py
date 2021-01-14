import datetime

from mongoengine import (
    DateTimeField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    LazyReferenceField,
    ListField,
    StringField,
)


class Parameter(Document):
    process_id = LazyReferenceField("Process", required=True)
    number_of_keeping_front_face = IntField(default=20, required=False)
    number_of_keeping_frontless_face = IntField(default=10, required=False)
    time_name = DateTimeField(required=False)

    camera_id_list = ListField()
    video_time_list = ListField()
    time_face_save_folder_list = ListField()
    time_face_save_folder_known_list = ListField()
    time_face_save_folder_unknown_list = ListField()
    time_save_videos_folder_list = ListField()
    time_save_data_folder_list = ListField()
    video_infor_list = ListField()
    front_face_angles = ListField(default=[90, 90, 90])

    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)

    meta = {"collection": "parameters"}
