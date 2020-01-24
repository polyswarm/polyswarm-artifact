from .schema import Schema
from pydantic import BaseModel, constr, AnyUrl, Json, IPvAnyAddress
from typing import Optional, List, Union

VersionStr = constr(regex="^\\d+\\.\\d+\\.\\d+$")

class Scanner(BaseModel):
    version: Optional[VersionStr]
    polyswarmclient_version: Optional[VersionStr]
    vendor_version: Optional[str]
    signatures_version: Optional[str]
    environment: Optional[Json]

    class Config:
        extra = True


class StixSignatures(BaseModel):
    class StixSignature(BaseModel):
        schema: str
        signature: Optional[Union[Json, str]]

        class Config:
            extra = True

    __root__: List[StixSignature]


class Verdict(Schema):
    malware_family: str
    domains: List[AnyUrl]
    ip_addresses: List[IPvAnyAddress]
    stix_signatures: Optional[StixSignatures]
    scanner: Optional[Scanner]

    class Config:
        extra = True
