import uvicorn
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status
from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.opportunities.opportunities_service import OpportunityService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.modules.contacts.contacts_service import ContactsService
from app.modules.database.database_aden_forms import AdenForms
from app.modules.landings.landings_service import LandingService
from app.constants.contacts_constants import ADD_ONE_FILE
from app.schemas.contacts_dto import UpdateContactDto
from app.schemas.landing_dto import CreateLandingDto
from app.schemas.env_schemas import (
    AppSchema,
    SalesForceSchema,
    GoogleDriveSchema,
    ContactsSchema,
    MysqlAdenFormsSchema
)
import os
import sys

app_settings = AppSchema(
    port=int(os.environ.get('APP_PORT')),
    host=os.environ.get('APP_HOST'),
    name_env=os.environ.get('NAME_ENV')
)

salesforce_settings = SalesForceSchema(
    sf_client_id=os.environ.get('SF_CLIENT_ID'),
    sf_client_secret=os.environ.get('SF_CLIENT_SECRET'),
    sf_redirect_uri=os.environ.get('SF_REDIRECT_URI'),
    sf_login_url=os.environ.get('SF_LOGIN_URL'),
    sf_user=os.environ.get('SF_USER'),
    sf_pass=os.environ.get('SF_PASS'),
    sf_password=os.environ.get('SF_PASSWORD'),
    sf_enviroment=os.environ.get('NAME_ENV')
)

gdrive_settings = GoogleDriveSchema(
    gd_scopes_url=[os.environ.get('DRIVE_SCOPE_URL')],
    gd_folder_id=os.environ.get('DRIVE_FOLDER_ID'),
    gd_client_email=os.environ.get('DRIVE_CLIENT_EMAIL'),
    # gd_private_key=os.environ.get('DRIVE_PRIVATE_KEY'),
)

contacts_settings = ContactsSchema(
    url_form=os.environ.get('URL_FORM')
)

mysql_aden_form_settings = MysqlAdenFormsSchema(
    mysql_host=os.environ.get('MYSQL_HOST'),
    mysql_port=int(os.environ.get('MYSQL_PORT')),
    mysql_user=os.environ.get('MYSQL_USER'),
    mysql_password=os.environ.get('MYSQL_PASSWORD'),
    mysql_db=os.environ.get('MYSQL_DB')
)

# instance of modules
# could not connect to the salesforce instance, exit program
salesforce_service = SalesForceService(salesforce_settings)
if not salesforce_service.connection:
    sys.exit()

# Opportunity instances
opportunity_service = OpportunityService(salesforce_service)

# Contact instaces
google_drive_service = GoogleDriveService(gdrive_settings)
contacts_service = ContactsService(
    contacts_settings=contacts_settings,
    google_drive=google_drive_service,
    salesforce=salesforce_service
)

# Landing instances
aden_forms_service = AdenForms(mysql_aden_form_settings)
landing_service = LandingService(
    aden_forms=aden_forms_service,
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
    if 'error' in opportunity:
        raise opportunity['error']
    else:
        return {"response_data": opportunity}


@app.get("/oportunities/amount/{id}", tags=['Opportunity'])
async def opportunity_amount(id: str):
    opportunity = opportunity_service.findOpportunityAmt(id=id)
    if 'error' in opportunity:
        raise opportunity['error']
    else:
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ADD_ONE_FILE)
    return {"response_data": contacts_service.uploadDocumentationDrive(
        salesforce_id=salesforce_id,
        student_name=student_name,
        files=files)}


# TODO: CACHE IT IN SOME WAY
@app.get('/contacts/form_inscription/link/{id}', tags=['Contacts'])
async def linkFormInscription(id: str):
    generate_link_form = contacts_service.generateLinkForm(id)
    if 'error' in generate_link_form:
        raise generate_link_form['error']
    else:
        return {"response_data": generate_link_form}


# TODO: CACHE IT IN SOME WAY
@app.get("/contacts/countries", tags=['Contacts'])
async def countryFormInscription():
    get_countries = contacts_service.getCountries()
    if 'error' in get_countries:
        raise get_countries['error']
    return {'response_data': get_countries}


# TODO: CACHE IT IN SOME WAY
@app.get("/contacts/utils-selects", tags=['Contacts'])
async def selectUtilsForm():
    get_selects_field = contacts_service.getSelectsField()
    if 'error' in get_selects_field:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unexpected error at getSelectsField'
        )
    return {'response_data': get_selects_field}


@app.get('/contacts/form_inscription/{id}', tags=['Contacts'])
async def formInscription(id: str):
    decodedId = contacts_service.decodeHashedIdtoSfId(hashId=id)
    if 'error' in decodedId:
        raise HTTPException(
            detail=decodedId.get('error'),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    get_form_inscription = contacts_service.getFormInscription(
        hashId=id,
        leadId=decodedId.get('id')
    )
    if 'error' in get_form_inscription:
        raise get_form_inscription['error']
    else:
        return {'response_data': get_form_inscription}


@app.patch('/contacts/form_inscription/{id}', tags=['Contacts'])
async def updateformInscription(id: str, updateContact: UpdateContactDto):
    decodedId = contacts_service.decodeHashedIdtoSfId(hashId=id)
    if 'error' in decodedId:
        raise HTTPException(
            detail=decodedId.get('error'),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    update_form_inscription = contacts_service.updateformInscription(
        formId=decodedId.get('id'),
        contactToUpdate=updateContact
    )
    if 'error' in update_form_inscription:
        raise update_form_inscription['error']
    else:
        return {'response_data': update_form_inscription}


@app.post('/landings', tags=['Landings'])
async def create(createLanding: CreateLandingDto):
    return {
        'response_data': landing_service.findOneInteresadoLanding(
            createLanding=createLanding
        )
    }


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
