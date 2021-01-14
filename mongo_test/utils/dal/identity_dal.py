from app.dal.base_dal import BaseDAL
from app.models import Identity


class IdentityDAL(BaseDAL):
    def __init__(self):
        super().__init__(Identity)
