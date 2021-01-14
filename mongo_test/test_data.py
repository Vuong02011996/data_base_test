from setting import *
from mongoengine import connect
from utils.dal import ObjectDAL
from bson import ObjectId

# MongoDB
connect(
    db=os.getenv("MONGO_DB_NAME"),
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
    authentication_source="admin",
    serverSelectionTimeoutMS=5000,
)

object_dal = ObjectDAL()
id = ObjectId("600005fd3d0298c66ab25407")
objs = list(object_dal.find_by_condition({"process": id}))
obj_ids = list(map(lambda e: e["id"], objs))
a = 0
# object_dal.delete({"id": {"$in": obj_ids}})
# detection_dal.delete({"object": {"$in": obj_ids}})

'''Test process : 600005fd3d0298c66ab25407'''