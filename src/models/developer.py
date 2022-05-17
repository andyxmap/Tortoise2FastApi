import re

from tortoise import fields

from src.models.base import Base
from src.models.project import Project

from tortoise.validators import RegexValidator
from tortoise.contrib.pydantic import pydantic_model_creator


class Developer(Base):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    git_repository = fields.TextField(validators=[RegexValidator('(?:https?://)?(?:www[.])?github[.]com/[\w-]+/?',re.I)])

    projects:fields.ReverseRelation[Project]

    class PydanticMeta:
        allow_cycles = True
        max_recursion = 4



Developer_Pydantic = pydantic_model_creator(Developer,name="Developer")
Developer_PydanticIN = pydantic_model_creator(Developer,name="Developer", exclude_readonly=True)
