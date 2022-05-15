from typing import List

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.util import parse2module, loader
from src.models.base import Base
from src.routers.builder import RouterBasedModel


# App based on yours selected tortoise model from
# construct crud api
class AppBasedModel(FastAPI):

    def configure(self, exclude: List[str] = ["Base"]):
        models = loader("src", Base, exclude=exclude)  # dynamic load
        for m in models:
            router = RouterBasedModel(m).build_crud_router()  # construct router based model
            self.include_router(router)


app = AppBasedModel()
app.configure()

register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": parse2module("src/models")},
    generate_schemas=True,
    add_exception_handlers=True,
)