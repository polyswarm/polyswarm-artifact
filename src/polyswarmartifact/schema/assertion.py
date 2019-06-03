import json
import os
import pkg_resources

from . import Schema
from .artifact import ArtifactEncoder


class Assertion(Schema):
    def __init__(self, ):
        self.artifacts = None

    def add_artifact(self, artifact):
        if self.artifacts is None:
            self.artifacts = []

        self.artifacts.append(artifact)
        return self

    @classmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return (
            pkg_resources.resource_filename(__name__, os.path.join('assertion.json')),
            'assertion'
        )

    def json(self):
        """
        Convert metadata implementation into json string
        :return: JSON string representing the internal type of this object
        """
        output = AssertionEncoder().encode(self)
        if not Assertion.validate(output):
            raise ValueError('Invalid Bounty setup')

        return output


class AssertionEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, Assertion):
            return json.dumps([ArtifactEncoder().encode(artifact) for artifact in obj.artifacts])
