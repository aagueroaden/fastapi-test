from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.schemas.env_schemas import ContactsSchema
from app.constants.contacts_constants import (
    CONTACTS_SERVICE_CITIZENSHIP,
    CONTACT_SOBJECT,
    FORMULARIO_INSCRIPCION_SOBJECT,
    CONTACT_SELECTS_FIELDS_NAMES,
    KEYS_OF_CONTACT_SELECTS_FIELDS_NAME,
    KEY_OF_FORM_INSCR_SELECTS_FIELDS_NAME
)

from fastapi import UploadFile, HTTPException, status
from typing import List
import base64
from app.utils.helpers.contacts import getNameAndFields


class ContactsService:

    def __init__(
            self,
            contacts_settings: ContactsSchema,
            google_drive,
            salesforce
    ) -> None:
        self._gdriveService: GoogleDriveService = google_drive
        self._salesforce: SalesForceService = salesforce
        self.baseUrl = contacts_settings.url_form

    def uploadDocumentationDrive(
            self,
            salesforce_id: str,
            student_name: str,
            files: List[UploadFile],
    ):
        response = []
        folderName = salesforce_id + "-" + student_name
        id = self._gdriveService.createFolder(folderName=folderName)

        if not id:
            return [{'error': 'failed to create the folder in google drive'}]

        for file in files:
            # """it will upload the file one at the time, maybe make it multiprosesing?"""
            response.append(self._gdriveService.uploadFile(file=file, folderId=id))
        return response

    # es re largo este, lo dejo para el final
    def getFormInscription(id: str):
        pass

    def generateLinkForm(self, id: str):
        id_to_ascii = id.encode("ascii")
        hash = base64.b64encode((id_to_ascii))
        hash_to_str = hash.decode("utf-8")
        return {
            "hash": hash_to_str,
            "base_url": self.baseUrl,
            "link": self.baseUrl + "/" + hash_to_str
        }

    def getCountries(self):
        response: dict = {}
        try:
            request = self._salesforce.requestHTTP(
                method='GET',
                endpoint=CONTACTS_SERVICE_CITIZENSHIP,
                data=''
            )
            if "fields" not in request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="there was a problem fetching the countries from salesforce, check endpoint"
                )
            fieldsContact: list = request.get("fields")
            for item in fieldsContact:
                if item['name'] == "hed__Citizenship__c":
                    fieldName, fieldValue = getNameAndFields(
                        name="hed__Citizenship__c",
                        item=item,
                        names_formatted=KEYS_OF_CONTACT_SELECTS_FIELDS_NAME,
                    )
                    response[fieldName] = fieldValue
                    # if already has all the data that it needs, stop looping
                    break

        except HTTPException as error:
            response = {'error': f'unexpected error in getCountries: {error}'}

        finally:
            return response

    def getSelectsField(self):
        response: dict = {}
        try:
            contact = self._salesforce.requestHTTP(
                method='GET',
                endpoint=CONTACT_SOBJECT,
                data=''
            )
            counter: int = 1
            fieldsContact: list = contact.get('fields')
            for item in fieldsContact:
                if item['name'] in CONTACT_SELECTS_FIELDS_NAMES:
                    fieldName, fieldValue = getNameAndFields(
                        name=item['name'],
                        item=item,
                        names_formatted=KEYS_OF_CONTACT_SELECTS_FIELDS_NAME
                    )
                    response[fieldName] = fieldValue

                    # if already has all the data that it needs, stop looping
                    counter += 1
                    if counter == len(KEYS_OF_CONTACT_SELECTS_FIELDS_NAME):
                        break

            form = self._salesforce.requestHTTP(
                method='GET',
                endpoint=FORMULARIO_INSCRIPCION_SOBJECT,
                data=''
            )

            fieldsFormInscrip: list = form.get("fields")
            for item in fieldsFormInscrip:
                if item['name'] == 'Estado_civil__c':
                    fieldName, fieldValue = getNameAndFields(
                        name='Estado_civil__c',
                        item=item,
                        names_formatted=KEY_OF_FORM_INSCR_SELECTS_FIELDS_NAME,
                    )
                    response[fieldName] = fieldValue
                    # if already has all the data that it needs, stop looping
                    break

        except Exception as error:
            response = {'error': f"unexpected error in getSelectsField: {error}"}

        finally:
            return response
