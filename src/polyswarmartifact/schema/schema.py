import logging
from typing import Union

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Schema(BaseModel):
    @classmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return cls.get_schema_json()

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.dict(exclude_unset=True, exclude_none=True) == other
        else:
            return super().__eq__(other)

    @classmethod
    def validate(cls, value):
        try:
            if isinstance(value, list):
                return cls.parse_obj(value)
            else:
                return BaseModel.validate(value)

        except pydantic.errors.DictError:
            raise ValueError
