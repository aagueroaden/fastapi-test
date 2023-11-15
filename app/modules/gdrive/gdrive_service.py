from app.schemas.env_schemas import GoogleDriveSchema


class GoogleDriveService:

    def __init__(self, settingsDrive: GoogleDriveSchema):
        self.drive = 'TODO'
        self.credentials = 'TODO'
        self.url = 'https://drive.google.com/drive/folders'
        self._scopes_url = settingsDrive.gd_scopes_url
        self._folder_id = settingsDrive.gd_folder_id
        self._client_email = settingsDrive.gd_client_email
        self._private_key = settingsDrive.gd_private_key

    def createFolder(self, folderName: str):
        pass

    def uploadFile(self, file, folderId: str):
        pass
