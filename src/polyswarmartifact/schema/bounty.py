from typing import List, Optional, Union

from pydantic import (
    AnyUrl,
    Field,
    PositiveInt,
    StrictStr,
    RootModel
)

from .schema import MD5, SHA1, SHA256, Schema


class FileArtifact(Schema):
    filename: Optional[str] = None
    filesize: Optional[PositiveInt] = None
    mimetype: StrictStr
    sha256: Optional[SHA256] = Field(title='SHA256', default=None)
    sha1: Optional[SHA1] = Field(title='SHA1', default=None)
    md5: Optional[MD5] = Field(title='MD5', default=None)


class URLArtifact(Schema):
    # protocol can actually be derived directly from `uri`, we keep it here to preserve a
    # preexisting interface.
    protocol: Optional[str]
    uri: AnyUrl = ...

    def __post_init__(self):
        if self.protocol is None:
            self.protocol = self.uri.protocol


class Bounty(RootModel, Schema):
    root: List[Union[FileArtifact, URLArtifact]] = Field(min_items=1, max_items=256, default=[])

    @property
    def artifacts(self):
        return self.root

    def add_file_artifact(self, **kwargs):
        self.root.append(FileArtifact(**kwargs))
        return self

    def add_url_artifact(self, uri: str = None, protocol: str = None):
        if uri is None:
            raise ValueError
        if protocol is not None:
            proto, *_ = protocol.rsplit('://', 1)
            uri = '{}://{}'.format(proto, next(reversed(uri.split('://', 1))))
        self.root.append(URLArtifact(uri=str(uri), protocol=protocol))
        return self

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
