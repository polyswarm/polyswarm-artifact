import pytest
from polyswarmartifact.schema import Schema


class TestSchema(Schema):
    @classmethod
    def get_schema(cls):
        return {}

    def json(self):
        super().json()


@pytest.mark.skip
def test_validate_no_class():
    with pytest.raises(NotImplementedError):
        Schema.validate({})


@pytest.mark.skip
def test_json():
    s = TestSchema()
    with pytest.raises(NotImplementedError):
        s.json()
