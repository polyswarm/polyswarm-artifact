from contextlib import contextmanager
from copy import deepcopy
import functools
import inspect
import logging
from typing import (
    Any,
    Callable,
    Collection,
    Mapping,
    NewType,
    Sequence,
    Set,
    Type,
    Union,
)

from pydantic import BaseModel, ValidationError, constr, validate_arguments

logger = logging.getLogger(__name__)

MD5 = constr(regex='^[0-9a-fA-F]{32}$', min_length=32, max_length=32)
SHA1 = constr(regex='^[0-9a-fA-F]{40}$', min_length=40, max_length=40)
SHA256 = constr(regex='^[0-9a-fA-F]{64}$', min_length=64, max_length=64)
Domain = constr(
    regex=r'(?:{int_chunk}\.)*?{int_chunk}{int_domain_ending}'.format(
        int_chunk=r'[_0-9a-\U00040000](?:[-_0-9a-\U00040000]{0,61}[_0-9a-\U00040000])?',
        int_domain_ending=r'(?P<tld>(\.[^\W\d_]{2,63})|(\.(?:xn--)[_0-9a-z-]{2,63}))?\.?',
    ),
    min_length=3,
    max_length=61 + 63 + 3
)
VersionStr = constr(regex=r"^[0-9]+([.][0-9]+)*$")


def chainable(fn: Callable):
    """
    Decorator to validate the arguments passed to a function, returning self
    """
    @validate_arguments
    @functools.wraps(fn)
    def setter_wrapper(self, *args: Any, **kwargs: Any) -> Any:
        fn(self, *args, **kwargs)
        return self

    return setter_wrapper


class Schema(BaseModel):
    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            with self.disable_validations():
                super().__init__()

    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError

    @classmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return cls.schema()

    @contextmanager
    def disable_validations(self):
        try:
            required_fields = set()
            for name, field in self.__class__.__fields__.items():
                if field.required is True:
                    required_fields.add(name)
                    field.required = False
            yield
        finally:
            for name in required_fields:
                self.__class__.__fields__[name].required = True

    def dict(self, *args, **kwargs):
        kwargs['exclude_none'] = True
        self.check_consistency()
        return super().dict(*args, **kwargs)

    @classmethod
    def validate(cls: Type['Schema'], value: Any, **kwargs) -> 'Union[Schema, bool]':
        try:
            return BaseModel.validate.__func__(cls, value).check_consistency()
        except ValidationError:
            return False

    def check_consistency(self) -> 'Schema':
        """Run all field validations on existing model"""
        errors = []
        fields = self.__fields__
        for k, v in fields.items():
            _, err = v.validate(getattr(self, k), fields, loc=k)
            if err:
                errors.append(err)
        if errors:
            raise ValidationError(errors, self.__class__)
        return self


class CollectionSchema(Schema):
    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
