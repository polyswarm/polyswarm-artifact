from typing import Any, Dict, List, Optional

from pydantic import Field, IPvAnyAddress, constr, validator

from .schema import Schema

VersionStr = constr(regex=r"^[0-9]+([.][0-9]+)*$")


class Scanner(Schema):
    version: Optional[VersionStr] = None
    polyswarmclient_version: Optional[VersionStr] = None
    vendor_version: Optional[str] = None
    signatures_version: Optional[str] = None
    environment: Optional[Dict] = None


class StixSignature(Schema):
    json_schema: str = Field(alias='schema')
    signature: Any

    def __getitem__(self, k):
        if k == 'schema':
            return self.json_schema
        return getattr(self, k)

    def dict(self, **kwargs):
        return super().dict(**{**kwargs, 'by_alias': True})


class Verdict(Schema):
    malware_family: str = None
    domains: Optional[List[str]] = []
    ip_addresses: Optional[List[IPvAnyAddress]] = []
    stix: Optional[List[StixSignature]] = []
    scanner: Optional[Scanner] = None

    @validator('scanner', pre=True)
    def _allow_empty_dict(cls, v):
        if not v:
            return None
        return v

    @property
    def extra(self):
        return [(k, v) for k, v in self.__dict__.items() if k not in self.__fields__]

    def add_domain(self, domain):
        self.domains.append(domain)
        return self

    def add_domains(self, domains):
        self.domains.extend(domains)
        return self

    def add_extra(self, key, value):
        setattr(self, key, value)
        return self

    def add_extras(self, extras):
        for k, v in extras:
            self.add_extra(k, v)
        return self

    def add_ip_address(self, ip_address):
        self.ip_addresses.append(ip_address)
        return self

    def add_ip_addresses(self, ip_addresses):
        for ip in ip_addresses:
            self.add_ip_address(ip)
        return self

    def add_stix_signature(self, schema, signature):
        self.stix.append(StixSignature(schema=schema, signature=signature))
        return self

    def add_stix_signatures(self, signatures):
        for schema, signature in signatures:
            self.add_stix_signature(schema, signature)
        return self

    def set_malware_family(self, malware_family: 'str'):
        self.malware_family = malware_family
        return self

    def set_scanner(self, **scanner):
        if 'operating_system' in scanner or 'architecture' in scanner:
            scanner["environment"] = {
                "operating_system": scanner.get("operating_system"),
                "architecture": scanner.get('architecture')
            }
            for k, v in scanner['environment'].items():
                if v is None:
                    del k

        self.scanner = Scanner(**scanner)
        return self

    class Config:
        extra = 'allow'
