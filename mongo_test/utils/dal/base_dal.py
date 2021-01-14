import datetime
from bson import ObjectId
from mongoengine import Document


class BaseDAL:
    def __init__(self, model_class: Document):
        self.model_class = model_class

        collection_name = self.model_class._meta["collection"]
        self.collection = self.model_class._get_db()[collection_name]

    def find_all(self):
        return list(self.collection.find())

    def find_by_id(self, _id):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        return self.collection.find_one({"_id": _id})

    def find_by_condition(self, condition: dict, sort=[], columns: dict = {}):
        return self.collection.find(condition).sort(sort)

    def find_one_by_condition(self, condition: dict):
        return self.collection.find(condition).first()

    def find_by_condition_one(self, condition: dict):
        return self.collection.find_one(condition)

    def create_one(self, data: dict, should_return_document=True):
        if hasattr(self.model_class, "created_at"):
            data["created_at"] = datetime.datetime.utcnow()

        self.model_class(**self.clone_ignore_id(data))
        item = self.collection.insert_one(data)

        if should_return_document:
            return self.find_by_id(item.inserted_id)

        return item.inserted_id

    def create_many(self, data: list):
        has_created_at = hasattr(self.model_class, "created_at")

        for i, element in enumerate(data):
            if has_created_at:
                data[i]["created_at"] = datetime.datetime.utcnow()

            self.model_class(**self.clone_ignore_id(element))

        return self.collection.insert_many(data)

    def update(self, condition: dict, data: dict, set_on_insert=None, push=None, upsert=False):
        self.model_class(**self.clone_ignore_id(data))
        update_data = {
            "$set": data,
        }
        if set_on_insert is not None:
            update_data["$setOnInsert"] = set_on_insert

        if push is not None:
            update_data["$push"] = push

        result = self.collection.update_many(condition, update_data, upsert=upsert)

        return result.modified_count

    def delete(self, condition: dict):
        result = self.collection.delete_many(condition)

        return result.deleted_count

    def aggregate(self, pipeline, kwargs=None):
        if kwargs is None:
            kwargs = {}

        return list(self.collection.aggregate(pipeline, **kwargs))

    @staticmethod
    def clone_ignore_id(data):
        data_clone = data.copy()
        data_clone.pop("_id", None)

        return data_clone
