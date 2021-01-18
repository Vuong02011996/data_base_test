from app.setting import *
import pymongo
from milvus import Milvus, DataType
from pprint import pprint
import numpy as np
from app.milvus_db import milvus_utils as mv
import time

# host = '14.241.120.239'
# port = '11037'

host = "localhost"
port = "19530"

milvus_client = Milvus(host, port)


username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
mongo_client = pymongo.MongoClient("mongodb://%s:%s@%s" % (username, password, host), 11038)


def create_collection_test(collection_test):
    collection_param_card = {
        "fields": [
            {
                "name": "facial_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 512}
            },
        ],
        "segment_row_limit": 10000,
        "auto_id": True
    }
    mv.create_collections(collection_test, collection_param_card)

    db = mongo_client.facial_recognition

    start_time = time.time()
    facial_data = db.detections.find({"facial_vector": {"$size": 512}})
    facial_vector = []
    for t in facial_data:
        facial_vector.append(t["facial_vector"])
        if len(facial_vector) == 1000000:
            break

    print(len(facial_vector))
    print("get data from mongo cost", time.time() - start_time)

    start_time = time.time()
    for i in range(0, len(facial_vector)):
        if i % 1000 == 0:
            facial_vector_insert = facial_vector[i:i + 1000]
            card_entities = [
                {"name": "facial_vector", "values": facial_vector_insert, "type": DataType.FLOAT_VECTOR},
            ]
            mv.milvus_client.insert(collection_test, card_entities)
    print("insert data to milvus cost", time.time() - start_time)


def create_collection_test_build_index(collection_test):
    collection_param_card = {
        "fields": [
            {
                "name": "facial_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 512}
            },
        ],
        "segment_row_limit": 10000,
        "auto_id": True
    }
    mv.create_collections(collection_test, collection_param_card)

    db = mongo_client.facial_recognition

    start_time = time.time()
    facial_data = db.detections.find({"facial_vector": {"$size": 512}})
    facial_vector = []
    for t in facial_data:
        facial_vector.append(t["facial_vector"])
        if len(facial_vector) == 1000000:
            break

    print(len(facial_vector))
    print("get data from mongo cost", time.time() - start_time)

    start_time = time.time()
    for i in range(0, len(facial_vector)):
        if i % 1000 == 0:
            facial_vector_insert = facial_vector[i:i + 1000]
            card_entities = [
                {"name": "facial_vector", "values": facial_vector_insert, "type": DataType.FLOAT_VECTOR},
            ]
            mv.milvus_client.insert(collection_test, card_entities)
    print("insert data to milvus cost", time.time() - start_time)

    # build index
    mv.milvus_client.create_index(collection_test, "facial_vector",
                        {"index_type": "IVF_FLAT", "metric_type": "IP", "params": {"nlist": 10}})

    info = mv.milvus_client.get_collection_info(collection_test)
    pprint(info)


def search_test(collection_name):
    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    facial_vector = []
    for t in facial_data[:10]:
        facial_vector.append(t["facial_vector"])
        break

    print(len(facial_vector), len(facial_vector[0]))

    dsl = {
        "bool": {
            "must": [
                {
                    "vector": {
                        "facial_vector": {"topk": 1, "query": facial_vector, "metric_type": "IP"}
                    }

                }
            ]
        }
    }

    results = milvus_client.search(collection_name, dsl)
    print("\n----------search----------")
    for entities in results:
        for top_dis in entities:
            print("- id: {}".format(top_dis.id))
            print("- similar: {}".format(top_dis.distance))


def search_test_build_index(collection_name):
    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    facial_vector = []
    for t in facial_data[:10]:
        facial_vector.append(t["facial_vector"])
        break

    print(len(facial_vector), len(facial_vector[0]))

    dsl = {
        "bool": {
            "must": [
                {
                    "vector": {
                        "facial_vector": {"topk": 1,
                                          "query": facial_vector,
                                          "metric_type": "IP",
                                          "params": {"nprobe": 20}}
                    }

                }
            ]
        }
    }

    results = milvus_client.search(collection_name, dsl)
    print("\n----------search----------")
    for entities in results:
        for top_dis in entities:
            print("- id: {}".format(top_dis.id))
            print("- similar: {}".format(top_dis.distance))


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
    # mv.crop_all_collection()

    collection_test = 'test'
    # create_collection_test(collection_test)
    start_time = time.time()
    search_test(collection_test)
    print("search no build index cost ", time.time() - start_time)
    '''
    ----------search----------
    - id: 1610075463456483778
    - distance: 0.4041309952735901
    '''
    collection_test_build_index = 'build_index'
    # create_collection_test_build_index(collection_test_build_index)
    mv.milvus_client.create_index(collection_test_build_index, "facial_vector",
                        {"index_type": "IVF_FLAT", "metric_type": "IP", "params": {"nlist": 100}})
    start_time = time.time()
    search_test_build_index(collection_test_build_index)
    print("search build index cost ", time.time() - start_time)


    # search_identity_card(collection_test)
    # test_get_entities_by_ids(collection_test)