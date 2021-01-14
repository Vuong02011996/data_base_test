from app.dal.base_dal import BaseDAL
from app.models import Logger


class LoggerDAL(BaseDAL):
    def __init__(self):
        super().__init__(Logger)
