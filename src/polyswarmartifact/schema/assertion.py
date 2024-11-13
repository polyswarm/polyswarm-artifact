from typing import List

from pydantic import Field, RootModel

from .schema import Schema, chainable
from .verdict import Verdict


class Assertion(RootModel, Schema):
    root: List[Verdict] = Field(min_items=1, max_items=256, default=[])

    @property
    def artifacts(self):
        return self.root

    @chainable
    def add_artifact(self, verdict: Verdict):
        self.root.append(verdict)

    @chainable
    def add_artifacts(self, verdicts: List[Verdict]):
        self.root.extend(verdicts)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
