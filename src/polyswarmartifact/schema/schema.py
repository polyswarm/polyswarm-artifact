import logging

from abc import ABC, abstractmethod
from jsonschema import validate, ValidationError

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
    def validate(cls, value, resolver=None, silent=False):
        """
        Validates a JSON value against the schema
        :param value: Dict or array to compare
        :param resolver: Optional resolver for finding references
        :param silent: Silence exception if silent is True
        :return: Boolean, True if JSON matches the schema
        """
        schema = cls.get_schema()
        try:
            validate(instance=value, schema=schema, resolver=resolver)
        except ValidationError:
            if not silent:
                logger.exception('Failed to validate schema')
            return False

        return True
