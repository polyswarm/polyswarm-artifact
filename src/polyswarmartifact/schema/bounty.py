from typing import List, Optional, Union

from pydantic import (
    AnyUrl,
    Field,
    PositiveInt,
    StrictStr,
    validator,
)

from .schema import MD5, SHA1, SHA256, Schema


class FileArtifact(Schema):
    filename: Optional[str] = Field(description='captures the filename of the artifact', default=None)
    filesize: Optional[PositiveInt] = Field(
        description='specifies the size of the artifact in bytes', default=None
    )
    mimetype: StrictStr = Field(description='indicates the type of media this file represents', default=-1)
    sha256: Optional[SHA256] = Field(title='SHA256', default=None)
    sha1: Optional[SHA1] = Field(title='SHA1', default=None)
    md5: Optional[MD5] = Field(title='MD5', default=None)


class URLArtifact(Schema):
    # protocol can actually be derived directly from `uri`, we keep it here to preserve a
    # preexisting interface.
    protocol: str = None
    uri: AnyUrl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.protocol is None:
            self.protocol = self.uri.protocol


class Bounty(Schema):
    __root__: List[Union[FileArtifact, URLArtifact]] = Field(min_items=1, max_items=256, default=[])

    @property
    def artifacts(self):
        return self.__root__

    def add_file_artifact(self, **kwargs):
        self.__root__.append(FileArtifact(**kwargs))
        return self

    def add_url_artifact(self, uri: str = None, protocol: str = None):
        if uri is None:
            raise ValueError
        if protocol is not None:
            proto, *_ = protocol.rsplit('://', 1)
            uri = '{}://{}'.format(proto, next(reversed(uri.split('://', 1))))
        self.__root__.append(URLArtifact(uri=str(uri), protocol=protocol))
        return self
