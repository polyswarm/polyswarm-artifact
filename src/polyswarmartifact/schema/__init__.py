import json
import logging
import os

from abc import ABC, abstractmethod
from jsonschema import validate, RefResolver, ValidationError

logger = logging.getLogger(__name__)


class Schema(ABC):
    @classmethod
    @abstractmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        raise NotImplementedError('get_schema is not implemented')

    @abstractmethod
    def json(self):
        """
        Convert metadata implementation into json string
        :return: JSON string representing the internal type of this object
        """
        raise NotImplementedError('json is not implemented')

    @classmethod
    def validate(cls, value):
        """
        Validates a JSON value against the schema
        :param value: Dict or array to compare
        :return: Boolean, True if JSON matches the schema
        """
        schema_path, schema_name = cls.get_schema()
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f'Cannot find schema_path: {schema_path}')

        with open(schema_path) as f:
            schema = json.loads(f.read())

        resolver = RefResolver(f'file://{schema_path}', schema_name)
        try:
            validate(instance=value, schema=schema, resolver=resolver)
        except ValidationError:
            logger.exception('Failed to validate schema')
            return False

        return True
