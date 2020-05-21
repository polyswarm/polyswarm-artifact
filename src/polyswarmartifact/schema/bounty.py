from typing import Mapping, Optional, Union

from pydantic import AnyUrl, PositiveInt, conlist, validator

from .schema import Md5, Schema, Sha1, Sha256


class FileArtifact(Schema):
    filename: Optional[str] = None
    filesize: Optional[PositiveInt] = None
    mimetype: str
    sha256: Optional[Sha256] = None
    sha1: Optional[Sha1] = None
    md5: Optional[Md5] = None


class URLArtifact(Schema):
    uri: AnyUrl

    def dict(self, *args, **kwargs):
        o = super().dict(*args, **kwargs)
        uri = o['uri']
        return {'protocol': f'{uri.scheme}://', 'uri': uri}


def distinguish(artifact: Mapping):
    for m in [FileArtifact, URLArtifact]:
        if any(f in artifact for f in m.__fields__):
            return m(**artifact)
    return artifact


class Bounty(Schema):
    __root__: conlist(Union[FileArtifact, URLArtifact], min_items=1, max_items=256) = []

    @validator('__root__', pre=True)
    def distinguish(cls, vs):
        if len(vs) > 0 and len(vs) < 256:
            return list(map(distinguish, vs))
        else:
            raise ValueError

    @property
    def artifacts(self):
        return self.__root__

    def add_file_artifact(self, **kwargs):
        self.artifacts.append(FileArtifact(**kwargs))
        return self

    def add_url_artifact(self, uri=None, protocol=None):
        if protocol is not None:
            proto, *_ = protocol.rsplit(':/', 1)
            uri = f'{proto}://{uri}'
        self.artifacts.append(URLArtifact(uri=uri))
        return self

    class Config:
        validate_assignment = True
