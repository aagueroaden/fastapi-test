import uvicorn
from fastapi import FastAPI, Depends
from typing import Annotated
from settings import envArgumentValidation, getEnvSettings

from app.salesforce.salesforce import SalesForceService

env = envArgumentValidation()
app_settings, salesforce_settings, auth_settings = getEnvSettings(env)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/salesforce")
async def salesforce():
    service = SalesForceService(salesforce_settings)
    print(service.connectPrimitive())
    return service.connect()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
