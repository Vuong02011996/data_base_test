from app.dal.base_dal import BaseDAL
from app.models import Camera


class CameraDAL(BaseDAL):
    def __init__(self):
        super().__init__(Camera)
