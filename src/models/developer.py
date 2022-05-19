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
    pro: fields.ReverseRelation[Project]

Developer_Pydantic = pydantic_model_creator(Developer,name="Developers")
Developer_PydanticIN = pydantic_model_creator(Developer,name="Developers", exclude_readonly=True)
