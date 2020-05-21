from typing import Optional, Union

from pydantic import AnyUrl, conlist, constr, PositiveInt

from .schema import Schema

MD5 = constr(min_length=32, max_length=32)
SHA1 = constr(min_length=40, max_length=40)
SHA256 = constr(min_length=64, max_length=64)


class FileArtifact(Schema):
    filename: Optional[str] = None
    filesize: Optional[PositiveInt] = None
    mimetype: str
    sha256: Optional[SHA256] = None
    sha1: Optional[SHA1] = None
    md5: Optional[MD5] = None


class URLArtifact(Schema):
    uri: AnyUrl

    def dict(self, *args, **kwargs):
        o = super().dict(*args, **kwargs)
        uri = o['uri']
        return {'protocol': f'{uri.scheme}://', 'uri': uri}


class Bounty(Schema):
    __root__: conlist(Union[FileArtifact, URLArtifact], min_items=1, max_items=256) = []

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
