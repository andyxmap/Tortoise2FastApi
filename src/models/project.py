from tortoise import fields
from src.models.base import Base

class Project(Base):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    developer = fields.ForeignKeyField('models.Developer', related_name='projects')

    class PydanticMeta:
        allow_cycles = True
        max_recursion = 2
        exclude = ["developer"]