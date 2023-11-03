from simple_salesforce import Salesforce
# from simple_salesforce import SalesforceLogin
import requests
from app.schemas.schemas import SalesForceSchema
from fastapi import HTTPException


token: str = ''
url: str = ''

# singleton
instanceConnection: bool = False


class SalesForceService:

    def __init__(self, settingsSF: SalesForceSchema) -> None:
        # self.userId: str = userId
        # self.orgId: str = orgId
        self.clientId: str = settingsSF.sf_client_id
        self.clientSecret: str = settingsSF.sf_client_secret
        self.redirectUri: str = settingsSF.sf_redirect_uri
        self.loginUrl: str = settingsSF.sf_login_url
        self.user: str = settingsSF.sf_user
        self.password: str = settingsSF.sf_password
        if not instanceConnection:
            self.connection: Salesforce = self._connect()

    # does not use any library
    def _connectPrimitive(self):
        payload = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'username': self.user,
            'password': self.password,
            'grant_type': 'password'
        }
        oauth_endpoint = '/services/oauth2/token'
        response = requests.post(self.loginUrl + oauth_endpoint, data=payload)
        print(response.status_code)
        testing = response.json()
        print(testing['access_token'])

    def _connect(self):
        try:
            sf_connection = Salesforce(
                username=self.user,
                password=self.password,
                consumer_key=self.clientId,
                consumer_secret=self.clientSecret,
                # instance_url=self.redirectUri,
                domain='test',  # This parameter allows the connection to the sandbox
            )
        except Exception | HTTPException as e:
            print(f"Connection ERROR {e}")
            print(f"cannot connect to {self.loginUrl}")
        print(f"connected to {self.loginUrl}")
        return sf_connection

    def executeQuery(self):
        pass

    async def requestHTTP(self):
        pass

    async def find(self):
        pass

    async def findFull(self):
        pass

    async def getById(self):
        pass

    async def create(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass

    async def upsert(self):
        pass

    async def describle(self):
        pass

    async def describeCache(self):
        pass

    async def describeCacheClear(self):
        pass

    async def describeGlobalCacheClear(self):
        pass

    async def clearCache(self):
        pass
