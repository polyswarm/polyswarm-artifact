from enum import Enum
import logging

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
        if not content:
            return None

        if self == ArtifactType.URL:
            return content.decode('utf-8')
        else:
            return content
