import pytest
from polyswarmartifact.schema import Schema


class TestSchema(Schema):
    @classmethod
    def get_schema(cls):
        return "./asdf", 'test'

    def json(self):
        super().json()


def test_validate_no_class():
    with pytest.raises(NotImplementedError):
        Schema.validate({})


def test_json():
    s = TestSchema()
    with pytest.raises(NotImplementedError):
        s.json()


def test_validate_bad_file():
    s = TestSchema()
    with pytest.raises(FileNotFoundError):
        s.validate({})
