# fastapicrud

Auto api crud based on tortoise models. Add dynamic classes import and parsed file location to py modules


## Installation


## Usage

Only just inherits from base which is a superclass of tortoise.models.Model

```python
from tortoise import fields

from src.models.base import Base


class Users(Base):
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
```

The core module will be in charge of dynamically loading and creating the endpoints according to the added models.
```python
class AppBasedModel(FastAPI):

    def configure(self, exclude: List[str] = ["Base"]):
        models = loader("src", Base, exclude=exclude)  # dynamic load
        for m in models:
            router = RouterBasedModel(m).build_crud_router()  # construct router based model
            self.include_router(router)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Contact me by email [mailto](mailto:violexmap@e.gmail.com)

## License
[MIT](https://choosealicense.com/licenses/mit/)
