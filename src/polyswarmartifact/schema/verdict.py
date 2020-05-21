from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, IPvAnyAddress, constr

from .schema import Schema

VersionStr = constr(regex=r"^[0-9]+([.][0-9]+)*$")

class Scanner(Schema):
    version: Optional[VersionStr] = None
    polyswarmclient_version: Optional[VersionStr] = None
    vendor_version: Optional[str] = None
    signatures_version: Optional[str] = None
    environment: Optional[Dict] = None


class StixSignature(Schema):
    stix_schema: str
    signature: str


class Verdict(Schema):
    malware_family: str = None
    domains: List[str] = []
    ip_addresses: List[IPvAnyAddress] = []
    stix: List[StixSignature] = []
    scanner: Optional[Scanner] = None

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
            setattr(self, k, v)
        return self

    def add_ip_address(self, ip_address):
        self.ip_addresses.append(ip_address)
        return self

    def add_ip_addresses(self, ip_addresses):
        self.ip_addresses.extend(ip_addresses)
        return self

    def add_stix_signature(self, schema, signature):
        self.stix.append({'schema': schema, 'signature': signature})
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
