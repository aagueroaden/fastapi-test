from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.schemas.env_schemas import ContactsSchema
from app.constants.contacts_constants import (
    CONTACTS_SERVICE_CITIZENSHIP,
    CONTACT_SOBJECT,
    FORMULARIO_INSCRIPCION_SOBJECT,
    CONTACT_SELECTS_FIELDS_NAMES,
    KEYS_OF_CONTACT_SELECTS_FIELDS_NAME,
    KEY_OF_FORM_INSCR_SELECTS_FIELDS_NAME,
    PROGRAM_NAME_ADEN_UNI,
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
        folderName = salesforce_id + " - " + student_name
        folderId = self._gdriveService.createFolder(folderName=folderName)

        if not folderId:
            return [{'error': 'failed to create the folder in google drive'}]

        for file in files:
            # """it will upload the file one at the time, maybe make it multiprosesing?"""
            response.append(self._gdriveService.uploadFile(file=file, folderId=folderId))
        return response

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

    def getFormInscription(self, hashId: str):
        try:
            leadId = base64.b64decode(hashId).decode("utf-8")
        except Exception:
            return {'error': f'The hashId provided: {hashId} , is an invalid hashId'}
        response = {}
        try:
            # search the opportunity
            lead = self._salesforce.executeQuery(
                f"""
                SELECT AccountId, Programa_acad_mico__c
                FROM Opportunity
                WHERE Id = '{leadId}'
                """
            )
            # if it didn't find anyhing with id= leadId
            if lead["totalSize"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Opportunity not found for id {leadId}"
                )

            # search the account associated to the opp of id leadId
            account = self._salesforce.executeQuery(
                f"""
                SELECT hed__Primary_Contact__c
                FROM Account
                WHERE Id = '{lead["AccountId"]}'
                """
            )

            # if it didn't find anything in that account
            if account["totalSize"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            # search the data of the account primary contact
            contact = self._salesforce.executeQuery(
                f"""
                SELECT Id, FirstName, LastName, Name, Email, hed__Country_of_Origin__c, Birthdate,
                    hed__Gender__c, Tipo_de_documento__c, Numero_de_documento__c,
                    Grupo_sangu_neo__c, RH__c, hed__Current_Address__c, Institucion_de_procedencia__c,
                    hed__AlternateEmail__c, Phone, OtherPhone, Nombre_del_acudiente__c,
                    Tel_particular_del_acudiente__c, Usuario_de_Instagram__c, Usuario_de_Facebook__c,
                    Actualmente_se_encuentra_laborando__c, Ocupaci_n_laboral__c, Estado_civil__c,
                    MailingStreet, MailingCity, MailingState, MailingPostalCode
                FROM Contact
                WHERE Id = '{account["hed__Primary_Contact__c"]}'
                """
            )

            # if it didn't find any contact with that account contact
            if contact["totalSize"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Contact not found"
                )

            if lead["Programa_acad_mico__c"]:
                program = self._salesforce.executeQuery(
                    f"""
                    SELECT Name
                    FROM Account
                    WHERE Id = '{lead["Programa_acad_mico__c"]}'
                    """
                )
                program_name = program["Name"] if program else PROGRAM_NAME_ADEN_UNI
            payments = self._salesforce.executeQuery(
                f"""
                SELECT Id, Cantidad_de_cuotas__c, CreatedById, Divisa__c, Forma_de_pago__c, Importe__c, Name,
                    Obtener_link_Forma_de_pago__c, Oportunidad__c, Respuesta_Hash__c, Respuesta_Link__c,
                    Respuesta_Tipo__c, Total_de_Formas_de_pago__c, LastModifiedById
                FROM Forma_de_pago__c
                WHERE Oportunidad__c = '{leadId}'
                AND Forma_de_pago__c = 'Online - Aden Checkout'
                """
            )
        except HTTPException as error:
            response = error

        finally:
            return response
