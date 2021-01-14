from bson import ObjectId

from app.dal.base_dal import BaseDAL
from app.models import Cluster


class ClusterDAL(BaseDAL):
    def __init__(self):
        super().__init__(Cluster)

    def find_by_element_obj(self, obj_id):
        assert isinstance(obj_id, ObjectId)

        return self.aggregate([
            {
                "$lookup": {
                    "from": "cluster_elements",
                    "localField": "_id",
                    "foreignField": "cluster",
                    "as": "cluster_elements",
                }
            },
            {
                "$match": {
                    "$or": [
                        {"cluster_elements.object": obj_id},
                        {"cluster_elements.ref_object": obj_id},
                    ],
                },
            },
            {
                "$lookup": {
                    "from": "identities",
                    "localField": "identity",
                    "foreignField": "_id",
                    "as": "identity",
                },
            },
            {
                "$project": {
                    "_id": 1,
                    "identity": 1,
                },
            }
        ])

    def get_by_ids_with_objects(self, ids):
        for _id in ids:
            assert isinstance(_id, ObjectId)

        return self.aggregate([
            {
                "$match": {"_id": {"$in": ids}}
            },
            {
                "$lookup": {
                    "from": "cluster_elements",
                    "localField": "_id",
                    "foreignField": "cluster",
                    "as": "elements",
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "objects": {
                        "$map": {
                            "input": "$elements",
                            "as": "element",
                            "in": "$$element.object"
                        }
                    }
                },
            },
        ])
