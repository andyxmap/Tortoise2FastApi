from tortoise import fields
from src.models.base import Base

class Event(Base):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')

