import json
import os
import pkg_resources

from . import Schema


class Verdict(Schema):
    def __init__(self):
        self.malware_family = None
        self.scanner = None
        self.domains = None
        self.ip_addresses = None
        self.stix = None
        self.extra = None

    def add_domain(self, domain):
        if self.domains is None:
            self.domains = []

        self.domains.append(domain)
        return self

    def add_domains(self, domains):
        if self.domains is None:
            self.domains = []

        self.domains.extend(domains)
        return self

    def add_extra(self, key, value):
        if self.extra is None:
            self.extra = []

        self.extra.append((key, value))

        return self

    def add_extras(self, extras):
        if self.extra is None:
            self.extra = []

        for k, v in extras:
            self.extra.append((k, v))

        return self

    def add_ip_address(self, ip_address):
        if self.ip_addresses is None:
            self.ip_addresses = []

        self.ip_addresses.append(ip_address)
        return self

    def add_ip_addresses(self, ip_addresses):
        if self.ip_addresses is None:
            self.ip_addresses = []

        self.ip_addresses.extend(ip_addresses)
        return self

    def add_stix_signature(self, schema, signature):
        if self.stix is None:
            self.stix = []

        self.stix.append({"schema": schema, "signature": signature})
        return self

    def add_stix_signatures(self, signatures):
        if self.stix is None:
            self.stix = []

        for schema, signature in signatures:
            self.stix.append({"schema": schema, "signature": signature})
        return self

    @classmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return pkg_resources.resource_filename(__name__, os.path.join('verdict.json')), 'verdict'

    def json(self):
        """
        Convert metadata implementation into json string
        :return: JSON string representing the internal type of this object
        """
        output = VerdictEncoder().encode(self)
        if not Verdict.validate(json.loads(output)):
            raise ValueError('Invalid Artifact setup')

        return output

    def set_malware_family(self, malware_family):
        self.malware_family = malware_family
        return self

    def set_scanner(self, operating_system=None, architecture=None, version=None, polyswarmclient_version=None,
                    signatures_version=None, vendor_version=None):
        scanner = {}

        if operating_system is not None or architecture is not None:
            scanner["environment"] = {
                "operating_system": operating_system,
                "architecture": architecture
            }

        if polyswarmclient_version is not None:
            scanner["polyswarmclient_version"] = polyswarmclient_version

        if version is not None:
            scanner["version"] = version

        if signatures_version is not None:
            scanner["signatures_version"] = signatures_version

        if vendor_version is not None:
            scanner['vendor_version'] = vendor_version

        self.scanner = scanner if scanner else None
        return self


class VerdictEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, Verdict):
            output = {
                "malware_family": obj.malware_family,
            }

            if obj.scanner:
                output["scanner"] = obj.scanner

            if obj.domains:
                output['domains'] = obj.domains

            if obj.ip_addresses:
                output['ip_addresses'] = obj.ip_addresses

            if obj.stix:
                output['stix'] = obj.stix

            if obj.extra:
                for key, value in obj.extra:
                    output[key] = value

            return json.dumps(output)
