from pydantic import BaseModel, PositiveInt, AnyUrl, Union
from typing import List, Optional
from .schema import Schema

MD5 = str
SHA1 = str
SHA256 = str

class FileArtifact(BaseModel):
    filename: Optional[str]
    filesize: Optional[PositiveInt]
    mimetype: str
    sha256: Optional[SHA256]
    sha1: Optional[SHA1]
    md5: Optional[MD5]

    class Config:
        extra = True


class URLArtifact(BaseModel):
    protocol: str
    uri: AnyUrl

    class Config:
        extra = True

class Bounty(Schema):
    __root__: List
    artifacts: List[Union[FileArtifact, URLArtifact]]

    def __init__(self, ):
        self.artifacts = []
