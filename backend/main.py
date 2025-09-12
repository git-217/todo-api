from fastapi import FastAPI
from backend.app.api.api import api_router


fastapi = FastAPI()
import backend.app.models


@fastapi.get('/', description='main path')
def main_page():
    return {"msg": "hello api!"}

fastapi.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(fastapi, host='127.0.0.1', port=8080, reload=True)