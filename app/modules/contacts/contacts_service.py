from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from fastapi import UploadFile, HTTPException, status
from typing import List


class ContactsService:

    def __init__(self, google_drive, salesforce) -> None:
        self._gdriveService: GoogleDriveService = google_drive
        self._salesforce: SalesForceService = salesforce

    def uploadDocumentationDrive(
            self,
            salesforce_id: str,
            student_name: str,
            files: List[UploadFile],
    ):
        "TODO: ERROR HANDLING"
        response = []
        if len(files) < 1:
            print("Need to add at least one file")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        folderName = salesforce_id + "-" + student_name
        id = self._gdriveService.createFolder(folderName=folderName)

        if not id:
            "TODO: ERROR"

        for file in files:
            """it will upload the file one at the time, maybe make it multiprosesing?"""
            response.append(self._gdriveService.uploadFile(file=file, folderId=id))
        return response
