from bson import ObjectId
import bson

from mongo_test.utils.dal.base_dal import BaseDAL
from mongo_test.utils.models import Object


class ObjectDAL(BaseDAL):
    def __init__(self, model=Object):
        super().__init__(model)

    def find_all_by_process(self, process_id):
        return self.aggregate(
            [
                {"$match": {"process": ObjectId(process_id)}},
                {
                    "$lookup": {
                        "from": "detections",
                        "localField": "_id",
                        "foreignField": "object",
                        "as": "detections",
                    },
                },
                # define suitable returned fields to minimize the bounding boxes
                {
                    "$project": {
                        "_id": 1,
                        "track_id": 1,
                        "finished_track": 1,
                        "avatar": 1,
                        "age": 1,
                        "gender": 1,
                        "from_frame": 1,
                        "to_frame": 1,
                        "from_time": 1,
                        "to_time": 1,
                        "detections._id": 1,
                        "detections.head_pose": 1,
                        "detections.frame_index": 1,
                        "detections.appeared_at": 1,
                        "detections.head_bbox": 1,
                        "detections.head_confidence": 1,
                        "detections.body_bbox": 1,
                        "detections.body_confidence": 1,
                        "detections.face_bbox": 1,
                        "detections.face_confidence": 1,
                    }
                },
            ]
        )

    def find_all_w_detection_by_process(self, process_id):
        return self.aggregate(
            [
                {"$match": {"process": ObjectId(process_id)}},
                {"$sort": {"track_id": 1}},
                {
                    "$lookup": {
                        "from": "detections",
                        "localField": "_id",
                        "foreignField": "object",
                        "as": "detections",
                    },
                },
                {
                    "$project": {
                        "_id": 1,
                        "track_id": 1,
                        "finished_track": 1,
                        "identity": 1,
                        "detection_first": {"$arrayElemAt": ["$detections", 0]},
                        "detection_last": {"$arrayElemAt": ["$detections", -1]},
                    }
                },
            ]
        )

    def find_all_identified_w_detection_by_process(self, process_id):
        return self.find_all_objects_w_detection_by_process(process_id, True)

    def find_all_unidentified_w_detection_by_process(self, process_id):
        return self.find_all_objects_w_detection_by_process(process_id, False)

    def find_all_objects_w_detection_by_process(self, process_id, is_identified: bool):
        return self.aggregate(
            [
                {"$match": {
                    "process": ObjectId(process_id),
                    "identity": {"$exists": is_identified},
                }},
                {
                    "$lookup": {
                        "from": "detections",
                        "localField": "_id",
                        "foreignField": "object",
                        "as": "detections",
                    },
                },
                {
                    "$project": {
                        "_id": 1,
                        "track_id": 1,
                        "ranges": 1,
                        "detections": 1,
                    }
                },
                # {
                #     "$group": {
                #         "_id": "$_id",
                #         "track_id": {"$first": "$track_id"},
                #         "ranges": {"$first": "$ranges"},
                #         "detections": {"$addToSet": "$detections"},
                #     }
                # },
                {"$sort": {"track_id": 1}},
            ],
            {"allowDiskUse": True}
        )

    def filter_by_process(self, process_id):
        """ Filter objects by process_id """
        return self.aggregate([{"$match": {"process": ObjectId(process_id)}}, {"$project": {"_id": 1, "identity": 1}}])

    def filter_by_cluster_element(self, cluster_type: str, ref_obj_id: ObjectId = None, cluster_id: ObjectId = None):
        if cluster_id:
            assert isinstance(cluster_id, ObjectId) or isinstance(cluster_id, bson.objectid.ObjectId)
        if ref_obj_id:
            assert isinstance(ref_obj_id, ObjectId) or isinstance(ref_obj_id, bson.objectid.ObjectId)

        conditions = {
            "cluster_elements.type": cluster_type,
            "$or": [
                {"objects.identity": None},
                {"objects.identity": {"$ne": True}},
            ],
        }
        if ref_obj_id is not None:
            conditions["cluster_elements.ref_object"] = ref_obj_id
        if cluster_id is not None:
            conditions["cluster_elements.cluster"] = cluster_id

        # TODO: Verify matching condition also filter objects collection, not just array of cluster_elements returning from lookup

        return self.aggregate([
            {
                "$lookup": {
                    "from": "cluster_elements",
                    "localField": "_id",
                    "foreignField": "object",
                    "as": "cluster_elements",
                },
            },
            {
                "$match": conditions,
            },
            {
                "$project": {
                    "_id": 1,
                    "uuid": 1,
                    "identity": 1,
                    "have_new_face": 1,
                    "have_new_body": 1,
                }
            },
        ])
