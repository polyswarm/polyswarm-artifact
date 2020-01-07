import json
import os
import pkg_resources
from jsonschema import RefResolver

from .schema import Schema
from .verdict import VerdictEncoder, VERDICT_SCHEMA

ASSERTION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "assertion",
    "type": "array",
    "minItems": 1,
    "maxItems": 256,
    "items": {"$ref": "verdict"}
}


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
        return ASSERTION_SCHEMA

    @classmethod
    def validate(cls, value, resolver=None, silent=False):
        resolver = RefResolver.from_schema(VERDICT_SCHEMA)
        return super().validate(value, resolver, silent)

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
