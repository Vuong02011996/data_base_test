from app.dal.base_dal import BaseDAL
from app.models import User
import logging
import os

from app.utils.common import logger_handler

# LOGGER
logger = logging.getLogger(__name__)
logger.addHandler(logger_handler())
logger.setLevel("DEBUG")
logger.propagate = False


class UserDAL(BaseDAL):
    def __init__(self):
        super().__init__(User)

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email})

