from tortoise import models
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from typing import Type, List


class Base(models.Model):

    @classmethod
    def to_pidantic(cls) -> Type[PydanticModel]:
        return pydantic_model_creator(cls, name=cls.__name__, allow_cycles=True)

    @classmethod
    def to_pidantic_no_id(cls) -> Type[PydanticModel]:
        return pydantic_model_creator(cls, exclude_readonly=True)

    @classmethod
    def list(cls) -> List[PydanticModel]:
        return cls.to_pidantic().from_queryset(cls.all())




