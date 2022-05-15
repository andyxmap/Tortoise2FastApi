from typing import TypeVar, Generic, Type, List
from src.models import base
from tortoise.contrib.pydantic import PydanticModel

TortoiseModelType = TypeVar("TortoiseModelType", bound=base.Base)
TortoiseResponsePydantic = TypeVar("TortoiseResponsePydantic", bound=PydanticModel)
TortoiseCreateSchemaPydantic = TypeVar("TortoiseCreateSchemaPydantic", bound=PydanticModel)
TortoiseUpdateSchemaPydantic = TypeVar("TortoiseUpdateSchemaPydantic", bound=PydanticModel)


class CRUD(Generic[TortoiseModelType, TortoiseResponsePydantic, TortoiseCreateSchemaPydantic, TortoiseUpdateSchemaPydantic]):
    def __init__(self, model: Type[TortoiseModelType]):
        self.model = model

    async def get_all(self) -> List[TortoiseResponsePydantic]:
        return await self.model.list()

    async def get_by_id(self, model_id: int) -> TortoiseResponsePydantic:
        query = self.model.get(id=model_id)
        return await self.model.to_pidantic().from_queryset_single(query)

    async def get_multi(self, offset: int, limit: int) -> List[TortoiseResponsePydantic]:
        query = self.model.all().offset(offset).limit(limit)
        return await self.model.to_pidantic().from_queryset(query)

    async def create(self, obj: TortoiseCreateSchemaPydantic) -> TortoiseResponsePydantic:
        created = await self.model.create(**obj.dict())
        return await self.model.to_pidantic().from_tortoise_orm(created)

    async def update(self, model_id: int, obj: TortoiseUpdateSchemaPydantic) -> TortoiseUpdateSchemaPydantic:
        await self.model.filter(id=model_id).update(**obj.dict())
        return await self.model.to_pidantic_no_id().from_queryset_single(self.model.get(id=model_id))

    async def deleted(self, model_id: int) -> TortoiseResponsePydantic:
        deleted_obj = await self.model.filter(id=model_id).delete()
        return deleted_obj


base = CRUD(base.Base)


