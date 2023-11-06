import uvicorn
from fastapi import FastAPI

from settings import envArgumentValidation, getEnvSettings

from app.salesforce.salesforce import SalesForceService

# loading env variables
env = envArgumentValidation()
app_settings, salesforce_settings, auth_settings = getEnvSettings(env)

# instance of fastapi
app = FastAPI()

# instance of models
salesforce_service = SalesForceService(salesforce_settings)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/salesforce")
async def salesforce():
    return {'session_id': salesforce_service.connection.session_id}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
