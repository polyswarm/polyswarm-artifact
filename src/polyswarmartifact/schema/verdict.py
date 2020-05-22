import itertools
from typing import Any, Dict, Iterable, List, Optional, Tuple

from pydantic import Field, IPvAnyAddress, StrictStr, validator

from .schema import Domain, Schema, VersionStr, chainable


def starmap(fn, iterable):
    return tuple(itertools.starmap(fn, iterable))


class Scanner(Schema):
    version: Optional[VersionStr] = None
    polyswarmclient_version: Optional[VersionStr] = Field(
        title='polyswarmclient package version', default=None
    )
    vendor_version: Optional[str] = None
    signatures_version: Optional[str] = Field(title='Engine signature version', default=None)
    environment: Optional[Dict[str, Optional[str]]] = Field(title='Analysis environment', default=None)


class StixSignature(Schema):
    stix_schema: str = Field(alias='schema')
    signature: Any  # what does this mean?

    @property
    def schema(self):
        return self.stix_schema

    def __getitem__(self, k):
        return getattr(self, k)

    def dict(self, *args, **kwargs):
        return super().dict(*args, **{**kwargs, 'by_alias': True})


class Verdict(Schema):
    malware_family: StrictStr = Field(default=-1)
    domains: Optional[List[Domain]] = Field(default=list())
    ip_addresses: Optional[List[IPvAnyAddress]] = Field(default=list())
    stix: Optional[List[StixSignature]] = Field(default=list())
    scanner: Optional[Scanner] = Field(default=None)

    @property
    def extra(self):
        return [(k, v) for k, v in self.__dict__.items() if k not in self.__fields__]

    @chainable
    def add_domain(self, domain: Domain):
        self.domains.append(domain)

    @chainable
    def add_domains(self, domains: Iterable[Domain]):
        self.domains.extend(domains)

    @chainable
    def set_malware_family(self, malware_family: str):
        self.malware_family = malware_family

    @chainable
    def add_extra(self, key: str, value: Any):
        setattr(self, key, value)

    @chainable
    def add_extras(self, extras: Iterable[Tuple[str, Any]]):
        return starmap(self.add_extra, extras)

    @chainable
    def add_ip_address(self, ip_address: IPvAnyAddress):
        self.ip_addresses.append(str(ip_address))

    @chainable
    def add_ip_addresses(self, ip_addresses: Iterable[IPvAnyAddress]):
        self.ip_addresses.extend(map(str, ip_addresses))

    @chainable
    def add_stix_signature(self, stix_schema: str, signature: Any):
        self.stix.append(StixSignature(schema=stix_schema, signature=signature))

    @chainable
    def add_stix_signatures(self, signatures: Iterable[Tuple[str, Any]]):
        return starmap(self.add_stix_signature, signatures)

    def set_scanner(self, **scanner):
        environment = {k: scanner.pop(k, None) for k in ('architecture', 'operating_system')}
        if any(environment.values()):
            scanner['environment'] = environment
        self.scanner = Scanner(**scanner)
        return self

    class Config:
        extra = 'allow'
