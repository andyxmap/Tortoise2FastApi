from typing import List, Type

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tortoise import Model, Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import ValidationError

from src.util import parse2module, loader
from src.models.base import Base
from src.routers.builder import RouterBasedModel


# App based on yours selected tortoise model from
# construct crud api
class AppBasedModel(FastAPI):

    def configure(self, exclude: List[str] = ["Base"], app_label="models"):
        Tortoise.init_models(parse2module("src"), app_label)
        models = loader("src", Base, exclude=exclude)  # dynamic load
        for m in models:
            router = RouterBasedModel(m).build_crud_router()  # construct router based model
            self.include_router(router)


class Router:
    def db_for_read(self, model: Type[Model]):
        return "slave"

    def db_for_write(self, model: Type[Model]):
        return "master"


app = AppBasedModel()
app.configure()


@app.exception_handler(ValidationError)
async def validation_exception_handler(__, exc: ValidationError):
    return JSONResponse(
                status_code=422,
                content={"detail": [{"loc": [], "msg": str(exc), "type": "ValidationError"}]}
    )


modules = [*parse2module("src/models"), "aerich.models"]



register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": parse2module("src/models")},
    generate_schemas=True,
    add_exception_handlers=True,
)

