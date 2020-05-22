import functools
import logging
from typing import (
    Any,
    Callable,
    Collection,
    Mapping,
    Sequence,
    Set,
    Type,
    Union,
    cast,
)

from pydantic import BaseModel, constr, validate_arguments, validator
from pydantic.decorator import ValidatedFunction

logger = logging.getLogger(__name__)

MD5 = constr(regex='^[0-9a-fA-F]{32}$', min_length=32, max_length=32)
SHA1 = constr(regex='^[0-9a-fA-F]{40}$', min_length=40, max_length=40)
SHA256 = constr(regex='^[0-9a-fA-F]{64}$', min_length=64, max_length=64)
Domain = constr(
    regex='(?:{int_chunk}\.)*?{int_chunk}{int_domain_ending}'.format(
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
    vd = ValidatedFunction(fn)

    @functools.wraps(fn)
    def setter_wrapper(*args: Any, **kwargs: Any) -> Any:
        vd.call(*args, **kwargs)
        return args[0]

    setter_wrapper.vd = vd  # type: ignore
    setter_wrapper.raw_function = vd.raw_function  # type: ignore
    setter_wrapper.model = vd.model  # type: ignore
    return cast(Callable, setter_wrapper)


class SchemaMeta(type(BaseModel)):
    def __new__(cls, name, bases, namespace, **kwargs):  # noqa C901
        annotations = namespace.get('__annotations__')

        if isinstance(annotations, Mapping) and '__root__' in annotations:
            models = annotations['__root__'].__args__
            if hasattr(models[0], '__args__'):
                models = models[0].__args__

            # map of each model to it's field names
            fields = {m: set(m.__fields__) for m in models}
            # create a set of all field values which are unique to their own model
            unique = functools.reduce(lambda a, b: a ^ b, fields.values(), set())

            @validator('__root__', pre=True, allow_reuse=True)
            def specialize_members(cls, members):  # noqa
                "Ensure that the field's name does not shadow an existing attribute of the model"
                for obj in members:
                    for m, fields in fields.items():
                        if fields & unique & obj.__fields__:
                            yield m.parse_obj(obj)

        return super().__new__(cls, name, bases, namespace, **kwargs)


class Schema(BaseModel, metaclass=SchemaMeta):
    @classmethod
    def get_schema(cls):
        """
        Get the path to the backing schema this Metadata object users
        :return: Tuple[string, string] where first string is the path,
        and the second is the schema name
        """
        return cls.schema()

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.dict(exclude_unset=True) == other
        else:
            return super().__eq__(other)

    def json(self, *args, **kwargs):
        self.parse_obj(self.dict(exclude_defaults=True))
        return super().json(*args, **kwargs)
