import importlib
import os
import warnings
from inspect import isclass
from os.path import curdir
from typing import List, Optional, Any
from tortoise import Tortoise
from fastapi import Path
from typing import Type
from src.models.base import Base

ROOT_DIR = os.path.dirname(os.path.abspath(curdir))


def tortoise_models():
    models = {}
    for _, models in Tortoise.apps.items():
        models = {key.lower(): val for key, val in models.items()}

    return models


def get_model(resource: Optional[str] = Path(...)) -> Type[Base]:
    for _, models in Tortoise.apps.items():
        for key, val in models.items():
            if resource.lower() == key.lower():
                return val


def get_pydantic_model(resource: Optional[str] = Path(...)):
    return get_model(resource).to_pidantic()


def __remove_extension(s: str):
    ext = '.py'
    return s.replace(ext, "")


def __remove_das(s: str):
    return s.replace("/", ".").replace("\\", ".")


def parse2module(p: str):
    f = []
    ext = '.py'
    for root, dirs, files in os.walk(os.path.join(ROOT_DIR, p)):
        for i in files:
            if not i.endswith(ext) or i.endswith("__init__.py"):
                continue
            module = root[root.find(p):]
            f.append("{0}.{1}".
                     format(__remove_das(module),
                            __remove_extension(i)))

    return f


def discover_base(
        base_path: str, base_type: Type[Any], alert=False, exclude: List[str] = []
    ) -> List[Type[Any]]:

    discovered_base = []

    try:
        module = importlib.import_module(base_path)
    except ImportError:
        raise Exception(f"{base_path} not found")

    possible_base = [getattr(module, attr_name) for attr_name in dir(module) if attr_name not in exclude]
    for attr in possible_base:
        if isclass(attr) and issubclass(attr, base_type):
            discovered_base.append(attr)

    if alert and not discovered_base:
        warnings.warn(f'"{base_path}" has no models', RuntimeWarning, stacklevel=4)

    return discovered_base


def loader(p: str, base_type, alert=False, exclude: List[str] = []):
    classes = []
    for m in parse2module(p):
        classes.extend(discover_base(m, base_type, alert, exclude))

    return set(classes)





