from src.core import app
import uvicorn


if __name__ == '__main__':
    uvicorn.run(app, port=5000, debug=True)
