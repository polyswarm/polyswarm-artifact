from typing import List, Optional, Union

from pydantic import AnyUrl, Field, PositiveInt, validator

from .schema import MD5, SHA1, SHA256, Schema


class FileArtifact(Schema):
    filename: Optional[str] = Field(description='captures the filename of the artifact', default=None)
    filesize: Optional[PositiveInt] = Field(
        description='specifies the size of the artifact in bytes', default=None
    )
    mimetype: str = Field(description='indicates the type of media this file represents')
    sha256: Optional[SHA256] = Field(title='SHA256', default=None)
    sha1: Optional[SHA1] = Field(title='SHA1', default=None)
    md5: Optional[MD5] = Field(title='MD5', default=None)


class URLArtifact(Schema):
    uri: AnyUrl

    def dict(self, *args, **kwargs):
        o = super().dict(*args, **kwargs)
        uri = o['uri']
        return {'protocol': f'{uri.scheme}://', 'uri': uri}


class Bounty(Schema):
    __root__: List[Union[FileArtifact, URLArtifact]] = Field(min_items=1, max_items=256, default=[])

    @property
    def artifacts(self):
        return self.__root__

    def add_file_artifact(self, **kwargs):
        self.__root__.append(FileArtifact(**kwargs))
        return self

    def add_url_artifact(self, uri: str, protocol: Optional[str] = None):
        if protocol is not None:
            proto, *_ = protocol.rsplit(':/', 1)
            uri = f'{proto}://{uri}'
        self.__root__.append(URLArtifact(uri=str(uri)))
        return self
