from typing import List

from pydantic import conlist

from .schema import Schema
from .verdict import Verdict


class Assertion(Schema):
    __root__: conlist(Verdict, min_items=1, max_items=256) = []

    @property
    def artifacts(self):
        return self.__root__

    def add_artifact(self, verdict: Verdict):
        self.__root__.append(verdict)
        return self

    def add_artifacts(self, verdicts: List[Verdict]):
        for verdict in verdicts:
            self.add_artifact(verdict)
        return self
