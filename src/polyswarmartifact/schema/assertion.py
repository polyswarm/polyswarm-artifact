from pydantic import BaseModel
from typing import List

from .schema import Schema
from .verdict import Verdict


class Assertion(Schema, BaseModel):
    artifacts: List[Verdict]
