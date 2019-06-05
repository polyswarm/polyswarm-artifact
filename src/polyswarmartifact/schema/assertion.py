import json
import os
import pkg_resources

from . import Schema
from .verdict import VerdictEncoder


class Assertion(Schema):
    def __init__(self, ):
        self.artifacts = []

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        return self

    def add_artifacts(self, artifacts):
        self.artifacts.extend(artifacts)
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
        if any([artifact is None for artifact in self.artifacts]):
            raise ValueError('Artifacts cannot be None')
        output = AssertionEncoder().encode(self)
        if not Assertion.validate(json.loads(output)):
            raise ValueError('Invalid Bounty setup')

        return output


class AssertionEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, Assertion):
            return json.dumps([json.loads(VerdictEncoder().encode(artifact)) for artifact in obj.artifacts])
