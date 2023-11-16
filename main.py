import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from typing import List

from settings import envArgumentValidation, getEnvSettings

from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.opportunities.opportunities_service import OpportunityService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.modules.contacts.contacts_service import ContactsService


# loading env variables
env, name_env = envArgumentValidation()
app_settings, salesforce_settings, gdrive_settings = getEnvSettings(env, name_env)


# instance of models
salesforce_service = SalesForceService(salesforce_settings)
opportunity_service = OpportunityService(salesforce_service)
google_drive_service = GoogleDriveService(gdrive_settings)
contacts_service = ContactsService(
    google_drive=google_drive_service,
    salesforce=salesforce_service
)

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


@app.post("/contacts/form_inscription/documentation", tags=['Contacts'])
async def form_inscription_documentation(
        files: List[UploadFile] = File(),  # this should be first parameter in the post...why? idk!
        salesforce_id: str = Form(),
        student_name: str = Form(),
        ):
    return contacts_service.uploadDocumentationDrive(
        salesforce_id=salesforce_id,
        student_name=student_name,
        files=files
    )


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
