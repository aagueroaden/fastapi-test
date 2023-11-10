from simple_salesforce import Salesforce
from fastapi import HTTPException, status
import requests
import urllib3
import json
from app.schemas.env_schemas import SalesForceSchema
token: str = ''
url: str = ''

# singleton?
instanceConnection: bool = False
http = urllib3.PoolManager()


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
        self.sf_enviroment: str = settingsSF.sf_enviroment
        if not instanceConnection:
            self.connection: Salesforce = self._connect()

    # does not use any library except request, just returns the token
    def connectPrimitive(self):
        payload = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'grant_type': 'password',
            'username': self.user,
            'password': self.password
        }
        response = requests.post(self.redirectUri, data=payload)

        json_res = response.json()
        access_token = json_res['access_token']
        return access_token

    def _connect(self):
        try:
            if self.sf_enviroment == 'test' or self.sf_enviroment == 'dev':
                sf_connection = Salesforce(
                    username=self.user,
                    password=self.password,
                    consumer_key=self.clientId,
                    consumer_secret=self.clientSecret,
                    domain='test',  # This parameter allows the connection to the sandbox
                )
            elif self.sf_enviroment == 'prod':
                sf_connection = Salesforce(
                    username=self.user,
                    password=self.password,
                    consumer_key=self.clientId,
                    consumer_secret=self.clientSecret,
                )
        except Exception as e:
            print(f"Connection ERROR {e}")
            print(f"cannot connect to {self.loginUrl}")
        print(f"connected to {self.loginUrl}")
        return sf_connection

    def executeQuery(self, query: str):
        response: dict = {}
        try:
            response = self.connection.query(query)
        except Exception as e:
            print(f"Error in executing the query: \n{e}")
            response = e
            raise HTTPException
        finally:
            return response

    def requestHTTP(self, method: str, endpoint: str, data: str | object):
        """
        method = 'GET' | 'POST' | etc...
        endpoint = some endpoint url
        data = an object of some kind | empty string if you wanna make a GET
        """
        try:
            auth = {'Authorization': 'Bearer ' + self.connection.session_id}
            response = http.request(
                body=data,
                method=method,
                headers=auth,
                url=self.loginUrl + endpoint
            )
            if response.status == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid auth Token"
                )
            if response.status == 200:
                return json.loads(response.data)
                # return response.json()
            else:
                print(response.status)
                return {}
        except HTTPException:
            if response.status == 401:
                print("Reconecting to salesforce...")
                self.connection = Salesforce(
                    instance=self.connection.sf_instance,
                    session_id=self.connection.session_id
                )
                return self.requestHTTP(method, endpoint, data)
            print("maybe salesforce secret is outdated?...")

    # does not seem to be used in salesforce nestjs api
    async def find(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def findFull(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def getById(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def create(self):
        pass

    # used by the student service module in salesforce nestjs api
    async def update(self):
        "TODO"
        pass

    # does not seem to be used in salesforce nestjs api
    async def delete(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def upsert(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def describe(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def describeCache(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def describeCacheClear(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def describeGlobalCacheClear(self):
        pass

    # does not seem to be used in salesforce nestjs api
    async def clearCache(self):
        pass
