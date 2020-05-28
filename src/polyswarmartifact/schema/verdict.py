from typing import Any, Dict, Iterable, List, Optional, Tuple

from pydantic import Field, IPvAnyAddress, StrictStr

from .schema import Domain, Schema, VersionStr, chainable


class Scanner(Schema):
    version: Optional[VersionStr] = Field(
        description="version of the microengine that generated the assertion"
    )
    polyswarmclient_version: Optional[VersionStr] = Field(description="version of polyswarmclient")
    vendor_version: Optional[str] = Field(description="version of the engine that generated the assertion")
    signatures_version: Optional[str] = Field(description="version of the engine's antimalware signatures")
    environment: Optional[Dict[str, Any]] = Field(description="analysis environment metadata")


class StixSignature(Schema):
    stix_schema: str = Field(alias='schema')
    signature: Any

    @property
    def schema(self):
        return self.stix_schema

    def dict(self, **kwargs):
        kwargs['by_alias'] = True
        return super().dict(**kwargs)


class Verdict(Schema):
    malware_family: StrictStr = Field(
        default=...,
        description='name of the malware family specified by this microengine',
    )
    domains: Optional[List[Domain]] = []
    ip_addresses: Optional[List[IPvAnyAddress]] = []
    stix: Optional[List[StixSignature]] = []
    scanner: Optional[Scanner]
    heuristic: Optional[bool] = Field(description='indicator for assertions generated from heuristics')

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
        for k, v in extras:
            self.add_extra(k, v)

    @chainable
    def add_ip_address(self, ip_address: IPvAnyAddress):
        self.ip_addresses.append(ip_address)

    @chainable
    def add_ip_addresses(self, ip_addresses: Iterable[IPvAnyAddress]):
        self.ip_addresses.extend(ip_addresses)

    @chainable
    def add_stix_signature(self, stix_schema: str, signature: Any):
        self.stix.append(StixSignature(schema=stix_schema, signature=signature))

    @chainable
    def add_stix_signatures(self, signatures: Iterable[Tuple[str, Any]]):
        for signature in signatures:
            self.add_stix_signature(*signature)

    @chainable
    def set_analysis_conclusion(self, heuristic: bool = None):
        if heuristic is not None:
            self.heuristic = heuristic

    def set_scanner(self, **scanner):
        environment = {k: scanner.pop(k, None) for k in ('architecture', 'operating_system')}
        if any(environment.values()):
            scanner.setdefault('environment', {}).update(environment)
        self.scanner = Scanner(**scanner)
        return self

    class Config:
        extra = 'allow'
