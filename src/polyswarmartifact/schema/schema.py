import logging

from pydantic import BaseModel, constr

logger = logging.getLogger(__name__)

Md5 = constr(regex='^[0-9a-fA-F]{32}$')
Sha1 = constr(regex='^[0-9a-fA-F]{40}$')
Sha256 = constr(regex='^[0-9a-fA-F]{64}$')


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

    def json(self, *args, **kwargs):
        self.parse_obj(self.dict())
        return super().json(*args, **kwargs)
