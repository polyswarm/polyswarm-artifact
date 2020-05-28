from typing import List

from pydantic import Field

from .schema import Schema, chainable
from .verdict import Verdict


class Assertion(Schema):
    __root__: List[Verdict] = Field(min_items=1, max_items=256, default=[])

    @property
    def artifacts(self):
        return self.__root__

    @chainable
    def add_artifact(self, verdict: Verdict):
        self.__root__.append(verdict)

    @chainable
    def add_artifacts(self, verdicts: List[Verdict]):
        self.__root__.extend(verdicts)

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
