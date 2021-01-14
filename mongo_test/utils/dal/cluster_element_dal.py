from app.dal.base_dal import BaseDAL
from app.models import ClusterElement


class ClusterElementDAL(BaseDAL):
    def __init__(self):
        super().__init__(ClusterElement)
