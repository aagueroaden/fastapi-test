from simple_salesforce import Salesforce
# from simple_salesforce import SalesforceLogin
import requests
from app.schemas.schemas import SalesForceSchema


class SalesForceService:

    # def __init__(
    #         self,
    #         # userId,
    #         # orgId,
    #         clientId,
    #         clientSecret,
    #         redirectUri,
    #         loginUrl,
    #         user,
    #         password,

    # ) -> None:
    #     # self.userId: str = userId
    #     # self.orgId: str = orgId
    #     self.clientId: str = clientId
    #     self.clientSecret: str = clientSecret
    #     self.redirectUri: str = redirectUri
    #     self.loginUrl: str = loginUrl
    #     self.user: str = user
    #     self.password: str = password

    def __init__(
            self,
            settingsSF: SalesForceSchema

    ) -> None:
        # self.userId: str = userId
        # self.orgId: str = orgId
        self.clientId: str = settingsSF.sf_client_id
        self.clientSecret: str = settingsSF.sf_client_secret
        self.redirectUri: str = settingsSF.sf_redirect_uri
        self.loginUrl: str = settingsSF.sf_login_url
        self.user: str = settingsSF.sf_user
        self.password: str = settingsSF.sf_password
        self.connect()

    def connectPrimitive(self):
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

    def connect(self):
        sf = Salesforce(
            username=self.user,
            password=self.password,
            consumer_key=self.clientId,
            consumer_secret=self.clientSecret,
            # instance_url=self.redirectUri,
            domain='test',  # This parameter allows the connection to the sandbox
        )
        print(sf.session_id)
        return {'session_id': sf.session_id}

    def login(self):
        pass

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

    async def describeCache(self):
        pass

    async def describeCacheClear(self):
        pass

    async def describeGlobalCacheClear(self):
        pass

    async def clear(self):
        pass


# if __name__ == '__main__':
#     SF_CLIENT_ID = '3MVG9QBLg8QGkFerS4zTdoCnaDJSqgN5hEzYxe1HpQ25vk0JcEdNWtgvX6LBIxnzMWBYw8XpQMoLS9ldjZ1iP'
#     SF_CLIENT_SECRET = 'AB6A92A56CC0C6C051C9305CEFA71733F36B9C5A647FBF923C740823837E9C68'
#     SF_REDIRECT_URI = 'https://adenuniversity--admins3.sandbox.my.salesforce.com/services/oauth2/token'
#     SF_LOGIN_URL = 'https://adenuniversity--admins3.sandbox.my.salesforce.com/'
#     SF_USER = 'admin.salesforce@aden.org.admins3'
#     SF_PASS = '4W7$kCDAwMr06MDQTSaFwwGuXRi8e4nKdfY'
#     SF_PASSWORD = '4W7$kCDAwM'
#     AUTH_SALESFORCE_API_KEY = 'eceebc33-e41b-4954-b639-86368773df77'
#     salesforceservice = SalesForceService(
#         clientId=SF_CLIENT_ID,
#         clientSecret=SF_CLIENT_SECRET,
#         redirectUri=SF_REDIRECT_URI,
#         loginUrl=SF_LOGIN_URL,
#         user=SF_USER,
#         password=SF_PASS,
#     )
#     # salesforceservice.connect()
#     # salesforceservice.anotherConnect()
