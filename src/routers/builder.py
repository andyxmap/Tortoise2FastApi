from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import Type, List, Optional

from tortoise.contrib.pydantic import PydanticModel
from src.models.base import Base
from src.util import get_model, get_pydantic_model
from src.crud import CRUD


def build_router() -> APIRouter:

    router = APIRouter()

    endpoints = ["/custom/{resource}/",
                 "/custom/{resource}/{model_id}",
                 "/custom/{resource}/create",
                 "/custom/{resource}/update/{model_id}",
                 "/custom/{resource}/delete/{model_id}"]

    responses = {404: {"model": HTTPNotFoundError}}

    @router.get(endpoints.pop(0), responses=responses)
    async def read_all(model: Type[Base] = Depends(get_model)):
        return await model.to_pidantic().from_queryset(model.all())

    @router.get(endpoints.pop(0), responses=responses)
    async def read(model_id: int, model: Type[Base] = Depends(get_model)):
        return await model.to_pidantic().from_queryset_single(model.get(id=model_id))

    @router.post(endpoints.pop(0), responses=responses)
    async def create(body_model: Type[PydanticModel] = Depends(get_pydantic_model), model: Type[Base] = Depends(get_model)):
        created = await model.create(**body_model.dict())
        return await model.to_pidantic().from_tortoise_orm(created)

    @router.put(endpoints.pop(0), responses=responses)
    async def update(model_id: int, body_model: Type[PydanticModel] = Depends(get_pydantic_model), model: Type[Base] = Depends(get_model)):
        await model.filter(id=model_id).update(**body_model.dict())
        return await model.to_pidantic_no_id().from_queryset_single(model.get(id=model_id))

    @router.delete(endpoints.pop(0), responses=responses)
    async def deleted(model_id: int, model: Type[Base] = Depends(get_model)):
        deleted_obj = await model.filter(id=model_id).delete()
        if not deleted_obj:
            raise HTTPException(status_code=404, detail=f"Object {model.__name__} by id= {model_id} not found ")
        return deleted_obj

    return router


class RouterBasedModel:

    model = None
    router = APIRouter()
    responses = {404: {"model": HTTPNotFoundError}}

    def __init__(self, model: Optional[Type[Base]] = None):

        self.model = model
        self.model_name = model.__name__.lower()
        self.pydantic_model = model.to_pidantic()

        self.endpoints = [
            f"/{self.model_name}/",
            f"/{self.model_name}/multi",
            "/{0}/{1}".format(self.model_name, "{model_id}"),
            "/{0}/create".format(self.model_name, "{model_id}"),
            "/{0}/update/{1}".format(self.model_name, "{model_id}"),
            "/{0}/delete/{1}".format(self.model_name, "{model_id}"),
            "/{0}/validate".format(self.model_name)
        ]

    def build_crud_router(self) -> Type[APIRouter]:
        # exclusive for type
        crud = CRUD(self.model)
        pydantic_model = crud.model.to_pidantic()
        pydantic_model_no_id = crud.model.to_pidantic_no_id()

        @self.router.get(self.endpoints.pop(0), response_model=List[pydantic_model], responses=self.responses)
        async def read_all():
            return await crud.get_all()

        @self.router.get(self.endpoints.pop(0), response_model=List[pydantic_model], responses=self.responses)
        async def get_multi(offset: Optional[int] = 0, limit: Optional[int] = 10):
            return await crud.get_multi(offset, limit)

        @self.router.get(self.endpoints.pop(0), response_model=pydantic_model, responses=self.responses)
        async def read(model_id: int):
            return await crud.get_by_id(model_id)

        @self.router.post(self.endpoints.pop(0), responses=self.responses)
        async def create(body_model:  pydantic_model):
            return await crud.create(body_model)

        @self.router.put(self.endpoints.pop(0), responses=self.responses)
        async def update(model_id: int, body_model: pydantic_model_no_id):
            return await crud.update(model_id, body_model)

        @self.router.delete(self.endpoints.pop(0), responses=self.responses)
        async def deleted(model_id: int):
            deleted_obj = await crud.deleted(model_id)
            if not deleted_obj:                                                                                       
                raise HTTPException(status_code=404, detail=f"Object {self.model.__name__} by id= {model_id} not found ")
            return deleted_obj

        @self.router.post(self.endpoints.pop(0))
        async def validate(obj: pydantic_model):
            r = await crud.validate(obj)
            if isinstance(r, str):
                return JSONResponse(content=r, status_code=422)

            return "ok"

        return self.router



