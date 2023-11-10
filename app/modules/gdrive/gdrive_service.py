from app.schemas.env_schemas import GoogleDriveSchema


class GoogleDriveService:

    def __init__(self, settingsDrive: GoogleDriveSchema):
        self.drive = 'TODO'
        self.auth = 'TODO'
        self.drive = 'TODO'
        self.url = 'https://drive.google.com/drive/folders'
        self._scopes_url = settingsDrive.gd_scopes_url
        self._folder_id = settingsDrive.gd_folder_id
        self._client_email = settingsDrive.gd_client_email
        self._private_key = settingsDrive.gd_private_key

    def createFolder(self, name: str):
        pass

    def uploadFile(self, file, folder_id: str):
        pass
