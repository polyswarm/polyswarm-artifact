import json
import os
import pkg_resources

from . import Schema
from .scanner import ScannerEncoder


class Microengine(Schema):
    def __init__(self, ):
        self.scanners = None

    def add_scanner(self, scanner):
        if self.scanners is None:
            self.scanners = []

        self.scanners.append(scanner)
        return self

    @classmethod
    def get_schema(cls, version):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return (
            pkg_resources.resource_filename(__name__, os.path.join(version, 'microengine.json')),
            'microengine'
        )

    def json(self):
        """
        Convert metadata implementation into json string
        :return: JSON string representing the internal type of this object
        """
        output = MicroengineEncoder().encode(self)
        if not Microengine.validate(output):
            raise ValueError('Invalid Microengine setup')

        return output


class MicroengineEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, Microengine):
            output = [ScannerEncoder().encode(scanner) for scanner in obj.scanners]

            return json.dumps(output)
