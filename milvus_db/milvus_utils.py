from milvus import Milvus, DataType
from pprint import pprint

# host = '14.241.120.239'
# port = '11037'

host = "192.168.111.133"
port = "11037"

milvus_client = Milvus(host, port, name="facial_recognition2")
milvus_client.close()
milvus_client = Milvus(host, port, name="facial_recognition2")

collection_bodies = 'bodies'
collection_faces = 'faces'
partition_identities = 'identities'
partition_objects = 'objects'


def define_collection_param_faces():
    collection_param_faces = {
        "fields": [
            {
                "name": "head_pose_range",
                "type": DataType.INT32
            },
            {
                "name": "facial_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 512}
            },
        ],
        "segment_row_limit": 4096,
        "auto_id": False
    }
    return collection_param_faces


def define_collection_param_bodies():
    collection_param_bodies = {
        "fields": [
            {
                "name": "uuid",
                "type": DataType.INT64
            },
            {
                "name": "body_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 512}
            },
            {
                "name": "cloth_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 128}
            },
            {
                "name": "hat_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 128}
            },
            {
                "name": "shoes_vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 128}
            },
        ],
        "segment_row_limit": 4096,
        "auto_id": True
    }

    return collection_param_bodies


def create_collections(collection_name, collection_param):
    if collection_name in milvus_client.list_collections():
        milvus_client.drop_collection(collection_name)
    milvus_client.create_collection(collection_name, collection_param)
    print(milvus_client.list_collections())


def create_partition(collection_name, partition_name):
    milvus_client.create_partition(collection_name, partition_name)
    pprint('Have partitions {} in collection {}'.format(milvus_client.list_partitions(collection_name), collection_name))


def crop_all_collection():
    for collection_name in milvus_client.list_collections():
        milvus_client.drop_collection(collection_name)


def create_table_for_face_rec():
    collection_param_faces = define_collection_param_faces()
    collection_param_bodies = define_collection_param_bodies()
    create_collections(collection_faces, collection_param_faces)
    create_collections(collection_bodies, collection_param_bodies)

    create_partition(collection_faces, partition_objects)
    create_partition(collection_faces, partition_identities)


if __name__ == '__main__':
    create_table_for_face_rec()