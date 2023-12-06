import uvicorn
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status

from settings import envArgumentValidation, getEnvSettings

from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.opportunities.opportunities_service import OpportunityService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.modules.contacts.contacts_service import ContactsService
from app.constants.contacts_constants import ADD_ONE_FILE
from app.schemas.contacts_dto import UpdateContactDto


# loading env variables
env, name_env = envArgumentValidation()
[
    app_settings,
    salesforce_settings,
    gdrive_settings,
    contacts_settings
] = getEnvSettings(env, name_env)


# instance of models
salesforce_service = SalesForceService(salesforce_settings)
opportunity_service = OpportunityService(salesforce_service)
google_drive_service = GoogleDriveService(gdrive_settings)
contacts_service = ContactsService(
    contacts_settings=contacts_settings,
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
async def uploadDocumentsFormInscription(
        # Files should be first parameter in the post...why? idk!
        titulo_bachiller: UploadFile = File(default=None),
        documento_identidad: UploadFile = File(default=None),
        solicitud_preconvalidacion: UploadFile = File(default=None),
        creditos_universidad: UploadFile = File(default=None),
        foto: UploadFile = File(default=None),
        salesforce_id: str = Form(),
        student_name: str = Form(),
        ):
    # did it like this to specify the files required
    files = [
        titulo_bachiller,
        documento_identidad,
        foto,
        solicitud_preconvalidacion,
        creditos_universidad
    ]
    files = [file for file in files if file is not None]
    if not files:
        return {"response_data": {'error': HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ADD_ONE_FILE
        )}}
    return {"response_data": contacts_service.uploadDocumentationDrive(
        salesforce_id=salesforce_id,
        student_name=student_name,
        files=files)}


# TODO: CACHE IT IN SOME WAY
@app.get('/contacts/form_inscription/link/{id}', tags=['Contacts'])
async def linkFormInscription(id: str):
    return {"response_data": contacts_service.generateLinkForm(id)}


# TODO: CACHE IT IN SOME WAY
@app.get("/contacts/countries", tags=['Contacts'])
async def countryFormInscription():
    return {'response_data': contacts_service.getCountries()}


# TODO: CACHE IT IN SOME WAY
@app.get("/contacts/utils-selects", tags=['Contacts'])
async def selectUtilsForm():
    return {'response_data': contacts_service.getSelectsField()}


@app.get('/contacts/form_inscription/{id}', tags=['Contacts'])
async def formInscription(id: str):
    if not id:
        return {"response_data": {'error': HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No hash given'
        )}}
    return {'response_data': contacts_service.getFormInscription(id)}


@app.patch('/contacts/form_inscription/{id}', tags=['Contacts'])
async def updateformInscription(id: str, updateContact: UpdateContactDto):
    return {
        'response_data': contacts_service.updateformInscription(
            hashId=id,
            contactToUpdate=updateContact
        )
    }

# TESTING FOR DTO AND VALIDATIONS WITH PYDANTIC
# from pydantic import BaseModel
# class Test(BaseModel):
#     esto_es_un_bool: bool = False
#     esto_es_un_string: str
#     interno: int

#     class Config:
#         json_schema_extra = {
#             'example': {
#                 'esto_es_un_bool': False,
#                 'esto_es_un_string': 'esto es un string',
#                 'interno': 12
#             },
#         }
# @app.put('/testing')
# async def test(data: Test):
#     return data


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
