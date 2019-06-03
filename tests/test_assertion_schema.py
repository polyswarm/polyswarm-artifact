import os
import json
import pytest
from polyswarmartifact.schema.assertion import Assertion
from polyswarmartifact.schema.verdict import Verdict


def test_get_schema_path_is_valid_file():
    # arrange
    # act
    path, name = Assertion.get_schema()
    # assert
    assert path == os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src", "polyswarmartifact", "schema", "assertion.json"))


def test_get_schema_name_matches_file():
    # arrange
    # act
    path, name = Assertion.get_schema()
    # assert
    assert name == "assertion"


def test_valid_blob_validates_true():
    # arrange
    blob = [
        {
            "malware_family": "Eicar",
        }
    ]
    # act
    result = Assertion.validate(blob)
    # assert
    assert result


def test_invalid_scanner_validates_false():
    # arrange
    blob = [
        {
            "malware_familty": None,
        }
    ]
    # act
    result = Assertion.validate(blob)
    # assert
    assert not result


def test_add_artifact():
    # arrange
    artifact = Verdict() \
        .set_malware_family("Eicar")
    assertion = Assertion()
    # act
    assertion.add_artifact(artifact)
    # assert
    assert assertion.artifacts and assertion.artifacts[0] == artifact


def test_builder_no_artifacts_throws_value_error():
    # arrange
    assertion = Assertion()
    # act
    with pytest.raises(ValueError):
        assertion.json()


def test_invalid_artifact_throws_value_error():
    # arrange
    artifact = Verdict()\
        .add_domain("polyswarm.io")
    # act
    assertion = Assertion()\
        .add_artifact(artifact)
    # assert
    with pytest.raises(ValueError):
        assertion.json()


def test_none_artifact_encodes_to_none():
    # arrange
    # act
    assertion = Assertion()\
        .add_artifact(None)
    # assert
    with pytest.raises(ValueError):
        assertion.json()


def test_builder_one_scanners_is_valid():
    # arrange
    artifact = Verdict()\
        .set_malware_family("Eicar")
    # act
    assertion = Assertion()\
        .add_artifact(artifact)
    # assert
    assert Assertion.validate(json.loads(assertion.json()))


def test_builder_256_scanners_is_valid():
    # arrange
    artifact = Verdict() \
        .set_malware_family("Eicar")
    assertion = Assertion()
    # act
    for i in range(0, 256):
        assertion.add_artifact(artifact)
    # assert
    assert Assertion.validate(json.loads(assertion.json()))
