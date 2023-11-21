from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.schemas.env_schemas import ContactsSchema
from app.constants.contacts_constants import CONTACTS_SERVICE_CITIZENSHIP
from fastapi import UploadFile, HTTPException, status
from typing import List
import base64
from app.utils.helpers.contacts import addLabelAndId


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
        response: list = []

        try:
            request = self._salesforce.requestHTTP(
                method='GET',
                endpoint=CONTACTS_SERVICE_CITIZENSHIP,
                data=''
            )
            if "fields" not in request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="there was a problem fetching the countries from salesforce"
                )
            fields = request.get("fields")
            for item in fields:
                if item['name'] == "hed__Citizenship__c":
                    allIdsAndLabelsofCountries = list(map(addLabelAndId, item['picklistValues']))
                    response = {'countries': allIdsAndLabelsofCountries}
                    break
                else:
                    continue

        except HTTPException as error:
            response = error

        finally:
            return response

    def getSelectsField(self):
        pass