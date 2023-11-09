import uvicorn
from fastapi import FastAPI


from settings import envArgumentValidation, getEnvSettings

from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.opportunities.opportunities_service import OpportunityService
# instance of fastapi
app = FastAPI()

# loading env variables
env = envArgumentValidation()
app_settings, salesforce_settings, auth_settings = getEnvSettings(env)


# instance of models
salesforce_service = SalesForceService(salesforce_settings)
opportunity_service = OpportunityService(salesforce_service)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/salesforce")
async def salesforce():
    return {'session_id': salesforce_service.connection.session_id}


@app.get("/querytest")
async def selectdata():
    mistring = '0017000000hOMChAAO'
    query_test = """
    SELECT Id, hed__Primary_Contact__c
    FROM Account
    WHERE Id = '{fid}'
    """.format(fid=mistring)
    return salesforce_service.executeQuery(query=query_test)


@app.get("/endpoint_test/{itemId}")
async def endpoint_test(itemId):
    # itemID example = '0066C00000J0c4VQAR'
    endpoint = "/services/data/v53.0/sobjects/Opportunity/" + itemId
    data = ''
    method = 'GET'
    return salesforce_service.requestHTTP(method=method, endpoint=endpoint, data=data)


@app.get("/oportunities/{id}")
async def oportunities(id: str):
    opportunity = opportunity_service.find0ne(id)
    return {"response_data": opportunity}

if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
