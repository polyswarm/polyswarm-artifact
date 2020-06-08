from typing import List

from pydantic import Field

from .schema import CollectionSchema, chainable
from .verdict import Verdict


class Assertion(CollectionSchema):
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
