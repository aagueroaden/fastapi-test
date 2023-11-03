import uvicorn
from fastapi import FastAPI

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
    return {'session_id': service.connection.session_id}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
