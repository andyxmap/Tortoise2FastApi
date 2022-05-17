from src.models.developer import Developer, Developer_Pydantic, Developer_PydanticIN
from src.crud.base import CRUD


class DeveloperCRUD(CRUD[Developer_Pydantic, Developer_Pydantic, Developer_PydanticIN, Developer_PydanticIN]):
    pass


developer = DeveloperCRUD(Developer)
