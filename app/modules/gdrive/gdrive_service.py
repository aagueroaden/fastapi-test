from app.schemas.env_schemas import GoogleDriveSchema
from app.constants.gdrive_constants import (
    SERVICE_ACCOUNT_FILE,
    GDRIVE_URL,
    FOLDER_MIME_TYPE,
    API_VERSION
)
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os 


class GoogleDriveService:

    def __init__(self, settingsDrive: GoogleDriveSchema):
        self.path: str = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_FILE)
        self.url: str = GDRIVE_URL
        self._scopes_url: list[str] = settingsDrive.gd_scopes_url
        self._folder_id: str = settingsDrive.gd_folder_id
        self._client_email: str = settingsDrive.gd_client_email
        self._private_key: str = settingsDrive.gd_private_key
        self.credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=self._scopes_url
        )
        self.drive = build('drive', API_VERSION, credentials=self.credentials)

    def createFolder(self, folderName: str):
        response = {}
        try:
            resource = {
                'name': folderName,
                'mimeType': FOLDER_MIME_TYPE,
                'parents': [self._folder_id],
            }
            # why the LSP does not detect the googleapi methods?
            response = self.drive.files().create(
                body=resource,
                fields='id'
            ).execute()
            print(f"Folder {folderName} created, id: {response['id']}")
            response = response['id']

        except Exception as error:
            print(f"Error creating the folder {folderName} in google drive")
            print(error)
            response = error

        finally:
            return response

    def uploadFile(self, file, folderId: str):
        folderUrl = GDRIVE_URL + "/" + folderId
        response = {}
        try:
            fileName = open(file=file, mode='rb').name
            fileMetadata = {
                'name': fileName,
                'parents': [folderId]
            }
            # mimetype=None to make it guess the mimetype itsef, instead of specifying 
            media = MediaFileUpload(fileName, resumable=True, mimetype=None)
            response = self.drive.files().create(
                body=fileMetadata,
                fields='id, name, mimeTyepe',
                media_body=media
            ).execute()
            response['folder_url'] = folderUrl

        except HttpError as error:
            print(f"Error uploading the file in the folder id: {folderId}")
            response = error

        finally:
            response
