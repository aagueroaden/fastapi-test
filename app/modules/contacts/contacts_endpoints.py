from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from app.schemas.contacts_dto import UpdateContactDto
from dependencies import contacts_service
from app.constants.contacts_constants import ADD_ONE_FILE

contacts_router = APIRouter()


@contacts_router.post(path="/contacts/form_inscription/documentation", tags=['Contacts'])
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
@contacts_router.get(path='/contacts/form_inscription/link/{id}', tags=['Contacts'])
async def linkFormInscription(id: str):
    generate_link_form = contacts_service.generateLinkForm(id)
    if 'error' in generate_link_form:
        raise generate_link_form['error']
    else:
        return {"response_data": generate_link_form}


# TODO: CACHE IT IN SOME WAY
@contacts_router.get(path="/contacts/countries", tags=['Contacts'])
async def countryFormInscription():
    get_countries = contacts_service.getCountries()
    if 'error' in get_countries:
        raise get_countries['error']
    return {'response_data': get_countries}


# TODO: CACHE IT IN SOME WAY
@contacts_router.get(path="/contacts/utils-selects", tags=['Contacts'])
async def selectUtilsForm():
    get_selects_field = contacts_service.getSelectsField()
    if 'error' in get_selects_field:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unexpected error at getSelectsField'
        )
    return {'response_data': get_selects_field}


@contacts_router.get(path='/contacts/form_inscription/{id}', tags=['Contacts'])
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


@contacts_router.patch(path='/contacts/form_inscription/{id}', tags=['Contacts'])
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
