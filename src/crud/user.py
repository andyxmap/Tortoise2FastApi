from src.models.user import Users, User_Pydantic, UserIn_Pydantic
from src.crud.base import CRUD


class User(CRUD[Users, User_Pydantic, User_Pydantic, UserIn_Pydantic]):
    pass


user = User(Users)
