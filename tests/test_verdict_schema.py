import json
import logging
import os

import pkg_resources
import pytest

from polyswarmartifact.schema.verdict import Verdict, __name__ as verdict_name

logger = logging.getLogger(__name__)


def test_get_schema_path():
    # arrange
    path, name = Verdict.get_schema()
    # act
    # assert
    assert path == pkg_resources.resource_filename(verdict_name, os.path.join('verdict.json'))


def test_get_schema_name():
    # arrange
    path, name = Verdict.get_schema()
    # act
    # assert
    assert name == "verdict"


def test_empty_verdict():
    # arrange
    verdict = Verdict()
    # act
    # assert
    with pytest.raises(ValueError):
        verdict.json()


def test_set_malware_family():
    # arrange
    verdict = Verdict()
    # act
    verdict.set_malware_family("Eicar")
    # assert
    assert verdict.malware_family == "Eicar"


def test_reset_malware_family():
    # arrange
    verdict = Verdict()
    verdict.set_malware_family("Eicar")
    # act
    verdict.set_malware_family("Trojan")
    # assert
    assert verdict.malware_family == "Trojan"


def test_validate_no_familty():
    # arrange
    verdict = Verdict()
    # assert
    with pytest.raises(ValueError):
        verdict.json()


def test_validate_with_family():
    # arrange
    verdict = Verdict()
    verdict.set_malware_family("Eicar")
    # assert
    blob = verdict.json()
    # act
    assert Verdict.validate(json.loads(blob))


def test_add_domain():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_domain('polyswarm.io')
    # assert
    assert verdict.domains == ['polyswarm.io']


def test_add_two_domains():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_domain('polyswarm.io')
    verdict.add_domain('polyswarm.network')
    # assert
    assert verdict.domains == ['polyswarm.io', 'polyswarm.network']


def test_validate_domains():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_domain('polyswarm.io')
    # assert
    assert Verdict.validate(json.loads(verdict.json()))


def test_add_ip():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_ip_address('192.168.0.1')
    # assert
    assert verdict.ip_addresses == ['192.168.0.1']


def test_add_two_ip():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_ip_address('192.168.0.1')
    verdict.add_ip_address('8.8.8.8')
    # assert
    assert verdict.ip_addresses == ['192.168.0.1', '8.8.8.8']


def test_validate_ip():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_ip_address('192.168.0.1')
    # assert
    assert Verdict.validate(json.loads(verdict.json()))


def test_validate_ip_invalid():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_ip_address('asdf')
    # assert
    with pytest.raises(ValueError):
        verdict.json()


def test_add_stix_object():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_stix(
        'oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json',
        "a0"
    )
    # assert
    assert verdict.stix[0]['schema'] == 'oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json'
    assert verdict.stix[0]['signature'] == "a0"


def test_add_stix_string():
    # arrange
    verdict = Verdict()
    # act
    verdict.add_stix('oasis-open/cti-stix2-json-schemas/master/schemas/common/hex.json', {
        "kill_chain_name": 'asdf',
        "phase_name": "full"
    })
    # assert
    assert verdict.stix[0]['schema'] == 'oasis-open/cti-stix2-json-schemas/master/schemas/common/hex.json'
    assert verdict.stix[0]['signature'] == {
        "kill_chain_name": 'asdf',
        "phase_name": "full"
    }


def test_validate_stix_object():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_stix(
        'oasis-open/cti-stix2-json-schemas/master/schemas/common/hex.json', {
            "kill_chain_name": 'asdf',
            "phase_name": "full"
        })
    # assert
    assert Verdict.validate(json.loads(verdict.json()))


def test_set_scanner_os():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows")
    # assert
    assert verdict.scanner == {
        "environment": {
            "operating_system": "windows",
            "architecture": None
        }
    }


def test_set_scanner_arch():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(architecure="x86")
    # assert
    assert verdict.scanner == {
        "environment": {
            "operating_system": None,
            "architecture": "x86"
        }
    }


def test_set_scanner_psc_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(polyswarmclient_version="1.1.1")
    # assert
    assert verdict.scanner == {
        "polyswarmclient_version": "1.1.1"
    }


def test_set_scanner_with_signature_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(signatures_version="05-12-2019")
    # assert
    assert verdict.scanner == {
        "signatures_version": "05-12-2019"
    }


def test_set_scanner_with_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(version="1.1.1")
    # assert
    assert verdict.scanner == {
        "version": "1.1.1"
    }


def test_set_scanner_with_vendor_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(vendor_version="1.1.1")
    # assert
    assert verdict.scanner == {
        "vendor_version": "1.1.1"
    }


def test_validate_scanner():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_no_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_null_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version=None, polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_invalid_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="asdf", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    with pytest.raises(ValueError):
        Verdict.validate(json.loads(verdict.json()))


def test_scanner_no_psc_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # assert
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0",
                        signatures_version="2019", vendor_version="1.0.0")
    # act
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_null_psc_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version=None,
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_invalid_psc_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="asdf",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    with pytest.raises(ValueError):
        Verdict.validate(json.loads(verdict.json()))


def test_scanner_no_signature_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_null_signature_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version=None, vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_no_vendor_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_null_vendor_version():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version=None)
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_null_environemnt():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_environemnt_no_os():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_environemnt_null_os():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system=None, architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_environemnt_no_arch():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", version="1.0.0", polyswarmclient_version="2.0.2",
                        signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_scanner_environemnt_null_arch():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.set_scanner(operating_system="windows", architecure="None", version="1.0.0",
                        polyswarmclient_version="2.0.2", signatures_version="2019", vendor_version="1.0.0")
    # assert
    Verdict.validate(json.loads(verdict.json()))


def test_add_extra_string():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_extra("new_key", "string_value")
    # assert
    k, v = verdict.extra[0]
    assert k == 'new_key'
    assert v == "string_value"


def test_add_extra_array():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_extra("new_key", ["string_value"])
    # assert
    k, v = verdict.extra[0]
    assert k == 'new_key'
    assert v == ["string_value"]


def test_add_extra_object():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_extra("new_key", {"other_key": "string_value"})
    # assert
    k, v = verdict.extra[0]
    assert k == 'new_key'
    assert v == {"other_key": "string_value"}


def test_validate_extra_string():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_extra("new_key", "string_value")
    # assert
    assert Verdict.validate(json.loads(verdict.json()))


def test_validate_extra_array():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_extra("new_key", ["string_value"])
    # assert
    assert Verdict.validate(json.loads(verdict.json()))


def test_validate_extra_object():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")
    # act
    verdict.add_extra("new_key", {"other_key": "string_value"})
    # assert
    assert Verdict.validate(json.loads(verdict.json()))


def test_validate_all_output():
    # arrange
    verdict = Verdict().set_malware_family("Eicar")\
        .add_domain('polyswarm.io')\
        .add_ip_address('192.168.0.1')\
        .add_stix(
        'oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json',
        "a0"
        ) \
        .set_scanner(operating_system="windows", architecure="x86", version="1.0.0", polyswarmclient_version="2.0.2",
                     signatures_version="2019", vendor_version="1.0.0")\
        .add_extra("new_key", {"other_key": "string_value"})\
        .add_extra("new_key1", ["string_value"])\
        .add_extra("new_key2", "string_value")

    result = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
        "new_key": {
            "other_key": "string_value",
        },
        "new_key1": ["string_value"],
        "new_key2": "string_value"
    }
    # act
    blob = json.loads(verdict.json())
    # assert
    assert Verdict.validate(blob)
    assert blob == result


def test_empty_domain_list():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": [],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_none_domain_list():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": None,
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_empty_ip_list():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": [],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_none_ip_list():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": None,
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_empty_stix_list():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_none_stix_list():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": None,
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_empty_scanner():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {}
    }
    # assert
    assert Verdict.validate(blob)


def test_none_scanner():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": None,
    }
    # assert
    assert Verdict.validate(blob)


def test_empty_environment():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {}
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_none_environment():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": None
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_string_scanner():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": "test",
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_array_scanner():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": ["test"],
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_object_scanner():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "extra": {"test": "tester"},
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_string_stix():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "extra": "test",
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_array_stix():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "extra": ["test"],
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_object_stix():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "extra": {"test": "tester"},
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_string_environment():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "extra": "test",
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_array_environment():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "extra": "test",
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)


def test_extra_object_environment():
    # arrange
    blob = {
        "malware_family": "Eicar",
        "domains": ["polyswarm.io"],
        "ip_addresses": ["192.168.0.1"],
        "stix": [{
            "schema": "oasis-open/cti-stix2-json-schemas/master/schemas/common/kill-chain-phase.json",
            "signature": "a0"
        }],
        "scanner": {
            "version": "1.0.0",
            "polyswarmclient_version": "2.0.2",
            "signatures_version": "2019",
            "vendor_version": "1.0.0",
            "environment": {
                "extra": "test",
                "operating_system": "windows",
                "architecture": "x86"
            }
        },
    }
    # assert
    assert Verdict.validate(blob)
