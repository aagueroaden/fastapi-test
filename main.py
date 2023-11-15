import uvicorn
from fastapi import FastAPI, Form
from typing import Annotated


from settings import envArgumentValidation, getEnvSettings

from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.opportunities.opportunities_service import OpportunityService
from app.modules.gdrive.gdrive_service import GoogleDriveService


# loading env variables
env, name_env = envArgumentValidation()
app_settings, salesforce_settings, gdrive_settings = getEnvSettings(env, name_env)


# instance of models
salesforce_service = SalesForceService(salesforce_settings)
opportunity_service = OpportunityService(salesforce_service)
google_drive_service = GoogleDriveService(gdrive_settings)

# instance of fastapi
app = FastAPI()


@app.get("/")
async def root():
    return {"SalesForce Fastapi, go to /docs to see the endpoints"}


@app.get("/oportunities/{id}", tags=['Opportunity'])
async def oportunities(id: str):
    opportunity = opportunity_service.find0ne(id=id)
    return {"response_data": opportunity}


@app.get("/oportunities/amount/{id}", tags=['Opportunity'])
async def opportunity_amount(id: str):
    opportunity = opportunity_service.findOpportunityAmt(id=id)
    return {"response_data": opportunity}


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

# @app.get("/salesforce")
# async def salesforce():
#     return {'session_id': salesforce_service.connection.session_id}


# @app.get("/querytest")
# async def selectdata():
#     mistring = '0017000000hOMChAAO'
#     query_test = """
#     SELECT Id, hed__Primary_Contact__c
#     FROM Account
#     WHERE Id = '{fid}'
#     """.format(fid=mistring)
#     return salesforce_service.executeQuery(query=query_test)


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
