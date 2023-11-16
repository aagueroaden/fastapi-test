from app.schemas.env_schemas import GoogleDriveSchema
from app.constants.gdrive_constants import (
    SERVICE_ACCOUNT_FILE,
    GDRIVE_URL,
    FOLDER_MIME_TYPE,
    API_VERSION
)
from google.auth.exceptions import MutualTLSChannelError
from fastapi import UploadFile
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from os import path
from io import BytesIO


class GoogleDriveService:

    def __init__(self, settingsDrive: GoogleDriveSchema):
        self.path: str = path.join(path.dirname(__file__), SERVICE_ACCOUNT_FILE)
        self.url: str = GDRIVE_URL
        self._scopes_url: list[str] = settingsDrive.gd_scopes_url
        self._folder_id: str = settingsDrive.gd_folder_id
        self._client_email: str = settingsDrive.gd_client_email
        self._private_key: str = settingsDrive.gd_private_key
        # self.credentials: service_account.Credentials = self._load_credentials()
        # self.drive = self._connect()
        self.credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=self._scopes_url
        )
        self.drive = build('drive', API_VERSION, credentials=self.credentials)

    def _load_credentials(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=self._scopes_url
            )
            return credentials

        except ValueError as error:
            print(f"could not load the credentials {error}")

    def _connect(self):
        try:
            drive = build('drive', API_VERSION, credentials=self.credentials)
            return drive

        except MutualTLSChannelError as error:
            print(f"error conecting to google drive: {error}")

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

        finally:
            return response

    def uploadFile(self, file: UploadFile, folderId: str):
        fh = BytesIO(file.file.read())
        folderUrl = GDRIVE_URL + "/" + folderId
        response = {}
        try:
            fileName = file.filename
            fileMetadata = {
                'name': fileName,
                'parents': [folderId]
            }
            media = MediaIoBaseUpload(
                fh,
                resumable=True,
                mimetype=file.headers['content-type'])
            response = self.drive.files().create(
                body=fileMetadata,
                fields='id, name, mimeType',
                media_body=media
            ).execute()
            response['folder_url'] = folderUrl

        except HttpError as error:
            print(f"Error uploading the file {file.filename} in the folder id: {folderId}")
            print(error)
            response = error

        except Exception as error:
            print(f"unexpected error uploading the file: {error}")
            response = error

        finally:
            return response
