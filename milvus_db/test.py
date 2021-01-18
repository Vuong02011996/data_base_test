from setting import *
import pymongo
from milvus import Milvus, DataType
from pprint import pprint
import numpy as np
from milvus_db import milvus_utils as mv
import time

# host = '14.241.120.239'
# port = '11037'


username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
mongo_client = pymongo.MongoClient("mongodb://%s:%s@%s" % (username, password, host), 11038)


def insert_entities(collection_name):
    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    head_pose = db.facial_data.find({"head_pose": {"$size": 3}})
    facial_vector = []
    for t in facial_data:
        facial_vector.append(t["facial_vector"])

    head_pose_range = []
    for t in head_pose:
        head_pose_range.append(t["head_pose"])

    uuid = np.arange(109)
    hybrid_entities = [
        # Milvus doesn't support string type yet, so we cannot insert "title".
        {"name": "uuid", "values": uuid, "type": DataType.INT64},
        {"name": "facial_vector", "values": facial_vector, "type": DataType.FLOAT_VECTOR},
    ]
    ids = milvus_client.insert(collection_name, hybrid_entities, partition_tag="identities")
    print("\n----------insert----------")
    print("Films are inserted and the ids are: {}".format(ids))


def create_collection_identity_card(collection_test):
    collection_param_card = {
        "fields": [
            {
                "name": "uuid",
                "type": DataType.INT64
            },
            {
                "name": "head_pose",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 3}
            },
            {
                "name": "facial_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 512}
            },
        ],
        "segment_row_limit": 4096,
        "auto_id": True
    }
    mv.create_collections(collection_test, collection_param_card)

    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    head_pose = db.facial_data.find({"head_pose": {"$size": 3}})
    facial_vector = []
    for t in facial_data[:3]:
        facial_vector.append(t["facial_vector"])

    head_pose_range = []
    for t in head_pose:
        head_pose_range.append(t["head_pose"])

    uuid = np.arange(109)
    card_entities = [
        {"name": "uuid", "values": uuid, "type": DataType.INT64},
        {"name": "head_pose", "values": head_pose_range, "type": DataType.FLOAT_VECTOR},
        {"name": "facial_vector", "values": facial_vector, "type": DataType.FLOAT_VECTOR},
    ]

    mv.milvus_client.insert(collection_test, card_entities)


def delete_ids_milvus(collection_name, list_ids):
    mv.milvus_client.delete_entity_by_id(collection_name, list_ids)


def get_entity_by_ids(collection_name, list_ids):
    mv.milvus_client.get_entity_by_id(collection_name, list_ids)


def search_identity_card(collection_name):
    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    head_pose = db.facial_data.find({"head_pose": {"$size": 3}})
    facial_vector = []
    for t in facial_data[0:1]:
        facial_vector.append(t["facial_vector"])
        break
    # list_head_pose = []
    # for t in head_pose[100:]:
    #     list_head_pose.append(t["head_pose"])
    #     break

    # vector_query = {
    #     "vector": {
    #         "topk": 10,
    #         "query": facial_vector,
    #         "metric_type": "L2"
    #     }
    # }
    # dsl = {
    #     "bool": {
    #         "must": [vector_query]
    #     }
    # }
    print(len(facial_vector), len(facial_vector[0]))


    dsl = {
        "bool": {
            "must": [
                {
                    # "vector": {
                    #     "head_pose": {"topk": 3, "query": list_head_pose, "metric_type": "IP"}
                    # },
                    "vector": {
                        "facial_vector": {"topk": 1, "query": facial_vector, "metric_type": "L2"}
                    }

                }
            ]
        }
    }

    # dsl = {
    #     "bool": {
    #         "must": [
    #             {
    #                 "term": {"uuid": [1, 2]}
    #             },
    #             {
    #                 "vector": {
    #                     "facial_vector": {"topk": 3, "query": facial_vector, "metric_type": "L2"}
    #                 }
    #             }
    #         ]
    #     }
    # }

    results = mv.milvus_client.search(collection_name, dsl, fields=['facial_vector', 'uuid'])
    print("\n----------search----------")
    for entities in results:
        for top_dis in entities:
            print("- id: {}".format(top_dis.id))
            print("- distance: {}".format(top_dis.distance))
            current_entity = top_dis.entity
            print("- facial_vector: {}".format(current_entity.facial_vector))
            print("- uuid: {}".format(current_entity.uuid))


def test_get_entities_by_ids(collection_name):
    # start_time = time.time()
    # identities_entities = milvus_client.get_entity_by_id(collection_name, [1609211744629965000, 1609211744629965000])
    # Error identity
    # face_entities = face_dal.get_entities(item["face_ids"])
    # list_facial_vector = []
    # for face_entity in face_entities:
    #     list_facial_vector.append(face_entity["facial_vector"])

    list_id = np.arange(1609213194831845000, 1609213194831845109)
    list_id = list(map(int, list_id))
    start_time = time.time()
    identities_entities = milvus_client.get_entity_by_id(collection_name, list_id)
    print(time.time() - start_time)

    start_time = time.time()
    for ids in list_id:
        identities_entities = milvus_client.get_entity_by_id(collection_name, [ids])
    print(time.time() - start_time)
    print(identities_entities)


if __name__ == '__main__':
    collection_test = 'card'
    # create_collection_identity_card(collection_test)

    list_ids = [1610939507631077000]
    delete_ids_milvus(collection_test, list_ids)
    result = get_entity_by_ids(collection_test, list_ids)
    search_identity_card(collection_test)
    print(result)



    # search_identity_card(collection_test)
    # test_get_entities_by_ids(collection_test)