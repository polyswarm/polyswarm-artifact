import pytest
from polyswarmartifact.schema import Schema


class TestSchema(Schema):
    @classmethod
    def get_schema(cls):
        return {}

    def json(self):
        super().json()
