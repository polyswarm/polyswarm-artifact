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

from pydantic import BaseModel, constr, validator

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
    # @validate_arguments
    @functools.wraps(fn)
    def setter_wrapper(self, *args: Any, **kwargs: Any) -> Any:
        fn(self, *args, **kwargs)
        return self

    return cast('Callable', setter_wrapper)


class SchemaMeta(type(BaseModel)):
    def __new__(cls, name, bases, namespace, **kwargs):  # noqa C901
        annotations = namespace.get('__annotations__')

        # the code below ensures only valid items are added to the container
        if isinstance(annotations, Mapping) and '__root__' in annotations:
            # Collect all this type can contain
            models = annotations['__root__'].__args__
            if hasattr(models[0], '__args__'):
                models = models[0].__args__

            # map of each model to it's field names
            fields = {m: set(m.__fields__) for m in models}
            # create a set of all unique field names to ensure we don't check a field name which
            # shadows an existing name.
            unique = functools.reduce(lambda a, b: a ^ b, fields.values(), set())
            fields = {m: f & unique for m, f in fields.items()}

            @validator('__root__', pre=True, allow_reuse=True)
            def specialize_members(cls, members):  # noqa
                "Ensure new members to this container object are valid"
                for obj in members:
                    for m, fields in fields.items():
                        if any(fields & obj.__fields__):
                            yield m.parse_obj(obj)
                        else:
                            raise ValueError

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

    def dict(self, *args, **kwargs):
        self.revalidate()
        return super().dict(*args, **kwargs)

    @classmethod
    def validate(cls: Type['Model'], value: Any) -> 'Model':
        try:
            return BaseModel.validate.__func__(cls, value).revalidate()
        except ValueError:
            return False

    def revalidate(self) -> 'Model':
        """Run all field validations on existing model"""
        ### FIXME: this code is kinda a mess, either remove it by verifying callers don't depend on
        ### it and `json` or figure out something clearer

        # handle container validation
        if hasattr(self, '__root__'):
            if any(not hasattr(v, 'validate') or not v.validate(v) for v in self.__root__):
                raise ValueError

        # and manually validate each field now
        for k, v in self.__fields__.items():
            _, err = v.validate(getattr(self, k), self.__fields__, loc=k)
            if err:
                raise ValueError

        return self
