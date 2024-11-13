import functools
import logging
from contextlib import contextmanager
from typing import (
    Any,
    Callable,
    Type,
    Union,
    cast,
)
from pydantic.fields import FieldInfo
from pydantic import BaseModel, ValidationError, constr, ConfigDict

logger = logging.getLogger(__name__)

MD5 = constr(pattern='^[0-9a-fA-F]{32}$', min_length=32, max_length=32)
SHA1 = constr(pattern='^[0-9a-fA-F]{40}$', min_length=40, max_length=40)
SHA256 = constr(pattern='^[0-9a-fA-F]{64}$', min_length=64, max_length=64)
Domain = constr(
    pattern=r'(?:{int_chunk}\.)*?{int_chunk}{int_domain_ending}'.format(
        int_chunk=r'[_0-9a-\U00040000](?:[-_0-9a-\U00040000]{0,61}[_0-9a-\U00040000])?',
        int_domain_ending=r'(?P<tld>(\.[^\W\d_]{2,63})|(\.(?:xn--)[_0-9a-z-]{2,63}))?\.?',
    ),
    min_length=3,
    max_length=61 + 63 + 3
)
VersionStr = constr(pattern=r"^[0-9]+([.][0-9]+)*$")


def chainable(fn: Callable):
    """
    Decorator to validate the arguments passed to a function, returning self
    """
    # @validate_arguments
    @functools.wraps(fn)
    def setter_wrapper(self, *args: Any, **kwargs: Any) -> Any:
        fn(self, *args, **kwargs)
        return self

    return setter_wrapper


class NoValidator:
    def validate_python(self, _, self_instance: BaseModel):
        object.__setattr__(self_instance, '__pydantic_fields_set__', set())
        object.__setattr__(self_instance, '__pydantic_extra__', {})
        object.__setattr__(self_instance, '__pydantic_private__', {})

        model_fields = cast(dict[str, FieldInfo], self_instance.model_fields)
        # print(model_fields)
        mapping = {}
        for field, info in model_fields.items():
            if not info.kw_only:
                if info.is_required():
                    mapping[field] = None
                else:
                    mapping[field] = info.get_default()
        for field, value in mapping.items():
            setattr(self_instance, field, value)
        return self_instance


class Schema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

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
        return cls.model_json_schema()

    @contextmanager
    def disable_validations(self):
        validator = self.__pydantic_validator__
        try:
            object.__setattr__(self, '__pydantic_validator__', NoValidator())
            yield
        finally:
            object.__setattr__(self, '__pydantic_validator__', validator)

    def __str__(self):
        return self.json()

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.dict(exclude_defaults=True) == other
        else:
            return super().__eq__(other)

    def dict(self, *args, by_alias=True, **kwargs):
        model_dict = super().model_dump(*args, **kwargs)
        super().model_validate(model_dict)
        return model_dict

    def json(self, *args, by_alias=True, **kwargs):
        kwargs.setdefault('exclude_defaults', True)
        # performing validation implicitly
        self.dict(*args, by_alias=by_alias, **kwargs)
        # use the custom json parser here
        return self.model_dump_json(*args, by_alias=by_alias, **kwargs)

    @classmethod
    def model_validate(cls: Type['BaseModel'], value: Any, **kwargs) -> 'Union[Schema, bool]':
        try:
            BaseModel.model_validate.__func__(cls, value)
        except ValidationError as e:
            logger.error(e)
            return False
        return True
