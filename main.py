import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import app_settings
from app.modules.landings.landings_endpoints import landings_router
from app.modules.opportunities.opportunities_endpoints import opportunities_router
from app.modules.contacts.contacts_endpoints import contacts_router

# instance of fastapi
app = FastAPI()

# routers
app.include_router(landings_router)
app.include_router(opportunities_router)
app.include_router(contacts_router)

# CORSMiddleware
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Generic Endpoint
@app.get("/")
async def root():
    return {"SalesForce Fastapi, go to /docs to see the endpoints"}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
