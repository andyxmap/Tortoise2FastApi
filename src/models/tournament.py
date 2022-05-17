from tortoise import fields

from src.models.base import Base
from src.models.event import Event


class Tournament(Base):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    events: fields.ReverseRelation[Event]