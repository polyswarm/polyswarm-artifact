from polyswarmartifact import ArtifactType


def test_file_artifact_type_from_lowercase_string():
    # arrange
    # act
    artifact_type = ArtifactType.from_string('file')
    # assert
    assert artifact_type == ArtifactType.FILE


def test_file_artifact_type_from_uppercase_string():
    # arrange
    # act
    artifact_type = ArtifactType.from_string('FILE')
    # assert
    assert artifact_type == ArtifactType.FILE


def test_url_artifact_type_from_lowercase_string():
    # arrange
    # act
    artifact_type = ArtifactType.from_string('url')
    # assert
    assert artifact_type == ArtifactType.URL


def test_url_artifact_type_from_uppercase_string():
    # arrange
    # act
    artifact_type = ArtifactType.from_string('URL')
    # assert
    assert artifact_type == ArtifactType.URL


def test_fake_artifact_type_from_uppercase_string():
    # arrange
    # act
    artifact_type = ArtifactType.from_string('fake')
    # assert
    assert artifact_type is None


def test_none_artifact_type():
    # arrange
    # act
    artifact_type = ArtifactType.from_string(None)
    # assert
    assert artifact_type is None


def test_file_artifact_type_to_string():
    # arrange
    # act
    # assert
    assert ArtifactType.to_string(ArtifactType.FILE) == 'file'


def test_url_artifact_type_to_string():
    # arrange
    # act
    # assert
    assert ArtifactType.to_string(ArtifactType.URL) == 'url'


def test_file_artifact_type_from_int():
    # arrange
    # act
    artifact_type = ArtifactType(0)
    # assert
    assert artifact_type == ArtifactType.FILE


def test_file_decode():
    # arrange
    # act
    # assert
    assert ArtifactType.FILE.decode_content(b'test string') == b'test string'


def test_url_artifact_type_from_int():
    # arrange
    # act
    artifact_type = ArtifactType(1)
    # assert
    assert artifact_type == ArtifactType.URL


def test_file_artifact_type_to_int():
    # arrange
    # act
    # assert
    assert ArtifactType.FILE.value == 0


def test_url_artifact_type_to_int():
    # arrange
    # act
    # assert
    assert ArtifactType.URL.value == 1


def test_url_decode():
    # arrange
    # act
    # assert
    assert ArtifactType.URL.decode_content(b'test string') == 'test string'


def test_url_decode_empty():
    # arrange
    # act
    # assert
    assert ArtifactType.URL.decode_content(b'') == ''


def test_url_decode_empty():
    # arrange
    # act
    # assert
    assert ArtifactType.URL.decode_content(None) == None
