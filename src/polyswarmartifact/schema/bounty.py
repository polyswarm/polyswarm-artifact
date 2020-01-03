import json

from jsonschema import RefResolver

from .schema import Schema

BOUNTY_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "bounty",
    "definitions": {
        "file": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "filesize": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "mimetype": {
                        "type": "string"
                    },
                    "sha256": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "sha1": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "md5": {
                        "type": [
                            "string",
                            "null"
                        ]
                    }
                },
                "additionalProperties": True,
                "required": [
                    "mimetype"
                ]
            }
        },
        "url": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "protocol": {"type": "string"}
                },
                "additionalProperties": True,
                "required": ["protocol"]
            }
        }
    },
    "type": "array",
    "oneOf": [
            {
                "$ref": "#/definitions/file"
            },
            {
                "$ref": "#/definitions/url"
            }
        ]
}


class Bounty(Schema):
    def __init__(self, ):
        self.artifacts = []

    def add_file_artifact(self, mimetype, filename=None, filesize=None, sha256=None, sha1=None, md5=None):
        if mimetype is None:
            raise ValueError("Mimetype cannot be None")
        artifact = {
            "mimetype": mimetype,
        }
        if filename is not None:
            artifact['filename'] = filename

        if filesize is not None:
            artifact['filesize'] = filesize

        if sha256 is not None:
            artifact['sha256'] = sha256

        if sha1 is not None:
            artifact['sha1'] = sha1

        if md5 is not None:
            artifact['md5'] = md5

        self.artifacts.append(artifact)
        return self

    def add_url_artifact(self, *_args, **kwargs):
        self.artifacts.append({**kwargs})
        return self

    @classmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return BOUNTY_SCHEMA

    def json(self):
        """
        Convert metadata implementation into json string
        :return: JSON string representing the internal type of this object
        """
        output = BountyEncoder().encode(self)
        if not Bounty.validate(json.loads(output)):
            raise ValueError('Invalid Bounty setup')

        return output

    @classmethod
    def validate(cls, value, resolver=None, silent=False):
        resolver = RefResolver.from_schema(BOUNTY_SCHEMA)
        return super().validate(value, resolver, silent)


class BountyEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, Bounty):
            return json.dumps([artifact for artifact in obj.artifacts])
