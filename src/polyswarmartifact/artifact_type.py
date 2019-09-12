import logging
from enum import Enum

from .exceptions import DecodeError

logger = logging.getLogger(__name__)


class ArtifactType(Enum):
    FILE = 0
    URL = 1

    @staticmethod
    def from_string(value):
        if value is not None:
            try:
                return ArtifactType[value.upper()]
            except KeyError:
                logger.critical('%s is not a supported artifact type', value)

    @staticmethod
    def to_string(artifact_type):
        return artifact_type.name.lower()

    def decode_content(self, content):
        if content is None:
            return None

        if self == ArtifactType.URL:
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                raise DecodeError('Error decoding URL')
        else:
            return content
