from app.dal.base_dal import BaseDAL
from app.models import Detection
from bson import ObjectId


class DetectionDAL(BaseDAL):
    def __init__(self, model=Detection):
        super().__init__(model)

    def filter_by_object(self, object_id):
        """ Return _id, frame_index, head_bbox and identity """
        return self.aggregate(
            [
                {"$match": {"object": ObjectId(object_id)}},
                {"$project": {"_id": 1, "frame_index": 1, "head_bbox": 1}},
            ]
        )

