import json
import os
import pkg_resources

from . import Schema


class Scanner(Schema):
    def __init__(self):
        self.malware_family = None
        self.microengine_info = None
        self.domains = None
        self.ip_addresses = None
        self.stix = None
        self.extra = None

    def add_domain(self, domain):
        if self.domains is None:
            self.domains = []

        self.domains.append(domain)
        return self

    def add_extra(self, key, value):
        if isinstance(value, dict):
            if self.extra is None:
                self.extra = []

            self.extra.append({key: value})

        return self

    def add_ip_address(self, ip_address):
        if self.ip_addresses is None:
            self.ip_addresses = []

        self.ip_addresses.append(ip_address)
        return self

    def add_stix(self, schema, signature):
        if self.stix is None:
            self.stix = []

        self.stix.push({"schema": schema, "signature": signature})
        return self

    @classmethod
    def get_schema(cls, version):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return pkg_resources.resource_filename(__name__, os.path.join(version, 'scanner.json')), 'scanner'

    def json(self):
        """
        Convert metadata implementation into json string
        :return: JSON string representing the internal type of this object
        """
        if self.version is None or self.malware_family is None or self.microengine_info is None:
            raise ValueError('Invalid Scanner setup')

        output = ScannerEncoder().encode(self)
        if not Scanner.validate(output):
            raise ValueError('Invalid Scanner setup')

        return output

    def set_malware_family(self, malware_family):
        self.malware_family = malware_family
        return self

    def set_microengine_info(self, operating_system, architecure,
                             polyswarmclient_version=None, microengine_version=None, signatures_version=None):
        self.microengine_info = {
            "environment": {
                "operating_system": operating_system,
                "architecture": architecure
            }
        }
        if polyswarmclient_version is not None:
            self.microengine_info["polyswarmclient_version"] = polyswarmclient_version

        if microengine_version is not None:
            self.microengine_info["polyswarmclient_version"] = microengine_version

        if signatures_version is not None:
            self.microengine_info["signatures_version"] = signatures_version


class ScannerEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, Scanner):
            output = {
                "malware_family": obj.malware_family,
                "microengine_info": obj.microengine_info
            }

            if obj.domains:
                output['domains'] = obj.domains

            if obj.ip_addresses:
                output['ip_addresses'] = obj.ip_addresses

            if obj.stix:
                output['stix'] = obj.stix

            if obj.extra:
                for key, value in obj.extra.items():
                    if isinstance(value, dict):
                        output[key] = value

            return json.dumps(output)
