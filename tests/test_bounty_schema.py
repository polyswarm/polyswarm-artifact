import os
import json

import pkg_resources
import pytest
from polyswarmartifact.schema.bounty import Bounty, __name__ as bounty_name


def test_get_schema_path_is_valid_file():
    # arrange
    # act
    path, name = Bounty.get_schema()
    # assert
    assert path == pkg_resources.resource_filename(bounty_name, os.path.join('bounty.json'))


def test_get_schema_name_matches_file():
    # arrange
    # act
    path, name = Bounty.get_schema()
    # assert
    assert name == "bounty"


def test_valid_blob_validates_true():
    # arrange
    blob = [
        {
            "mimetype": "text/plain",
        }
    ]
    # act
    result = Bounty.validate(blob)
    # assert
    assert result


def test_invalid_scanner_validates_false():
    # arrange
    blob = [
        {
            "filesize": "0",
        }
    ]
    # act
    result = Bounty.validate(blob)
    # assert
    assert not result


def test_add_file_artifact():
    # arrange
    bounty = Bounty()
    artifact = {
        "mimetype": "text/plain"
    }
    # act
    bounty.add_file_artifact(mimetype="text/plain")
    # assert
    assert bounty.artifacts and bounty.artifacts[0] == artifact


def test_add_url_artifact():
    # arrange
    bounty = Bounty()
    artifact = {
        "protocol": "https://"
    }
    # act
    bounty.add_url_artifact(protocol="https://")
    # assert
    assert bounty.artifacts and bounty.artifacts[0] == artifact
    assert bounty.json() == json.dumps([artifact])


def test_add_both_artifact():
    # arrange
    bounty = Bounty()
    # act
    bounty.add_url_artifact(protocol="https://")
    bounty.add_file_artifact(mimetype="test")
    # assert

    with pytest.raises(ValueError):
        bounty.json()


def test_add_full_artifact():
    # arrange
    bounty = Bounty()
    artifact = {
        "mimetype": "text/plain",
        "filename": "file",
        "filesize": "0",
        "sha256": "sha256",
        "sha1": "sha1",
        "md5": "md5"

    }
    # act
    bounty.add_file_artifact(mimetype="text/plain", filename="file", filesize="0", sha256="sha256", sha1="sha1", md5="md5")
    # assert
    assert bounty.artifacts and bounty.artifacts[0] == artifact


def test_builder_no_artifacts_empty_list():
    # arrange
    bounty = Bounty()
    # act
    # assert
    with pytest.raises(ValueError):
        bounty.json()


def test_invalid_artifact_throws_value_error():
    # arrange
    # act
    bounty = Bounty()\
        .add_file_artifact(mimetype=0)
    # assert
    with pytest.raises(ValueError):
        bounty.json()


def test_builder_one_scanners_is_valid():
    # arrange
    # act
    bounty = Bounty() \
        .add_file_artifact(mimetype="text/plain")
    # assert
    assert Bounty.validate(json.loads(bounty.json()))


def test_builder_256_scanners_is_valid():
    # arrange
    bounty = Bounty()
    # act
    for i in range(0, 256):
        bounty.add_file_artifact(mimetype="text/plain", filename="file", filesize=f"{i}", sha256="sha256", sha1="sha1",
                                 md5="md5")
    # assert
    assert Bounty.validate(json.loads(bounty.json()))
