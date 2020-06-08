import pprint

import pytest

from polyswarmartifact.schema import Assertion, Bounty, Verdict, FileArtifact, URLArtifact


@pytest.mark.parametrize('klass', [Assertion, Bounty, Verdict, FileArtifact, URLArtifact])
def test_schema_generation(klass):
    schema = klass.schema()
    assert isinstance(schema, dict)
    assert schema == klass.get_schema()
