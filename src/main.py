from src.core import app
import uvicorn

from src.routers.builder import RouterBasedModel
from src.models.empresa import Empresa


if __name__ == '__main__':
    uvicorn.run(app, port=5000, debug=True)
