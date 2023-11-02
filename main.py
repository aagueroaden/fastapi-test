import uvicorn
from fastapi import FastAPI

from salesforce import SalesForceService



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/salesforce")
async def salesforce():
    service = SalesForceService(
    )
    return service.get()


if __name__ == '__main__':
    env = envArgumentValidation()
    env_settings, salesforce_settings, auth_settings = getEnvSettings(env)
    uvicorn.run(
        app,
        host=env_settings.host,
        port=env_settings.port,
        reload=True
    )
