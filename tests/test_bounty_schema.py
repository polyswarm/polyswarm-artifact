import json

import pytest
from polyswarmartifact.schema.bounty import Bounty


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
            "filesize": "1",
        }
    ]
    with pytest.raises(ValueError):
        # act
        result = Bounty.validate(blob)


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
        "protocol": "https://",
        "uri": 'https://google.com'
    }
    # act
    bounty.add_url_artifact(protocol="https://", uri='google.com')
    # assert
    assert bounty.artifacts and bounty.artifacts[0] == artifact
    assert bounty.json() == json.dumps([artifact])


@pytest.mark.skip
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
        "filesize": 1,
        'sha256': "74b4147957813b62cc8987f2b711ddb31f8cb46dcbf71502033da66053c8780a",
        'sha1': "f013d66c7f6817d08b7eb2a93e6d0440c1f3e7f8",
        'md5': "772ac1a55fab1122f3b369ee9cd31549"
    }
    # act
    bounty.add_file_artifact(mimetype="text/plain", filename="file", filesize=1,
                                 sha256="74b4147957813b62cc8987f2b711ddb31f8cb46dcbf71502033da66053c8780a",
                                 sha1="f013d66c7f6817d08b7eb2a93e6d0440c1f3e7f8",
                                 md5="772ac1a55fab1122f3b369ee9cd31549")
    # assert
    assert bounty.artifacts and bounty.artifacts[0].dict() == artifact


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
    # assert
    with pytest.raises(ValueError):
        bounty = Bounty()\
            .add_file_artifact(mimetype=0)
        bounty.json()


def test_invalid_mime_throws_value_error():
    # arrange
    # act
    # assert
    with pytest.raises(ValueError):
        Bounty().add_file_artifact(mimetype=None)


def test_builder_one_scanners_is_valid():
    # arrange
    # act
    bounty = Bounty() \
        .add_file_artifact(mimetype="text/plain")
    # assert
    assert Bounty.validate(bounty.dict())


def test_builder_256_scanners_is_valid():
    # arrange
    bounty = Bounty()
    # act
    for i in range(1, 256):
        bounty.add_file_artifact(mimetype="text/plain",
                                 filename="file",
                                 filesize=str(i),
                                 sha256="74b4147957813b62cc8987f2b711ddb31f8cb46dcbf71502033da66053c8780a",
                                 sha1="f013d66c7f6817d08b7eb2a93e6d0440c1f3e7f8",
                                 md5="772ac1a55fab1122f3b369ee9cd31549",)
    # assert
    assert Bounty.validate(bounty.dict())
