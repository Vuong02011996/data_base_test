from app.dal.base_dal import BaseDAL
from app.models import Parameter


class ParameterDAL(BaseDAL):
    def __init__(self):
        super().__init__(Parameter)
