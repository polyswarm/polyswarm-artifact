from enum import Enum

import logging

logger = logging.getLogger(__name__)


class ArtifactType(Enum):
    FILE = 0
    URL = 1

    @staticmethod
    def from_string(value):
        try:
            return ArtifactType[value.upper()]
        except KeyError:
            logger.critical(f'{value} is not a supported artifact type')

    @staticmethod
    def to_string(artifact_type):
        return artifact_type.name.lower()
