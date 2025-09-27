from fastapi import FastAPI
import uvicorn
from app.api.api import api_router


app = FastAPI()


@app.get("/", description="main path")
def main_page() -> dict:
    return {"msg": "hello api!"}


app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
