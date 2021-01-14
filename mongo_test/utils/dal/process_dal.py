from app.dal.base_dal import BaseDAL
from app.models import Process


class ProcessDAL(BaseDAL):
    def __init__(self):
        super().__init__(Process)

    def get_next_uuid(self):
        element = list(self.collection.find().sort([("uuid", -1)]).limit(1))

        if len(element) == 0:
            return 1

        uuid = element[0]["uuid"] + 1 if element[0].get("uuid") is not None else 1

        return uuid
