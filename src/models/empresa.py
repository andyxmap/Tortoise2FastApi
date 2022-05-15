from tortoise import fields

from src.models.base import Base


class Empresa(Base):

    name = fields.TextField()
    description = fields.TextField()




