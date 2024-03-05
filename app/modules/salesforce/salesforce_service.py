from simple_salesforce import Salesforce, SFType
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
        self.clientId: str = settingsSF.sf_client_id
        self.clientSecret: str = settingsSF.sf_client_secret
        self.redirectUri: str = settingsSF.sf_redirect_uri
        self.loginUrl: str = settingsSF.sf_login_url
        self.user: str = settingsSF.sf_user
        self.password: str = settingsSF.sf_password
        self.sf_enviroment: str = settingsSF.sf_enviroment
        self.connection: Salesforce | None = self._connect()

    # does not use any library except request, just returns the token
    def _connectPrimitive(self):
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
            print(f"connected to {self.loginUrl}")
            return sf_connection

        except Exception as e:
            print(f"Connection ERROR {e}")
            print(f"cannot connect to {self.loginUrl}, check credentials")
            return None

    def executeQuery(self, query: str) -> None | list:
        response = None
        try:
            response = self.connection.query(query)
            # bad query input
            if "totalSize" not in response:
                raise HTTPException

            # didnt find anything with that query
            elif response["totalSize"] == 0:
                response = None

            # find one or more records on the query
            else:
                response = response["records"]

        except HTTPException as e:
            print(f"Error in executing the query: \n{e}")
            response = None

        finally:
            return response

    def requestHTTP(self, method: str, endpoint: str, data: str | object):
        """
        method = 'GET' | 'POST' | etc... BUT NOT PUT
        endpoint = some endpoint url
        data = an object of some kind | empty string if you wanna make a GET
        """
        try:
            auth = {'Authorization': 'Bearer ' + self.connection.session_id}
            if method == "POST":
                auth = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.connection.session_id
                }
                data = json.dumps(data)
            response = http.request(
                body=data,
                method=method,
                headers=auth,
                url=self.loginUrl + endpoint
            )
            print(response.data)
            if response.status == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid auth Token"
                )
            elif response.status == 200:
                return json.loads(response.data)
            elif response.status in [404, 400]:
                return {}
            else:
                print(f"salesforce  http response status: {response.status}")
                data = json.loads(response.data)
                return data

        except HTTPException:
            if response.status == 401:
                print("Reconecting to salesforce...")
                self.connection = self._connect()
                return self.requestHTTP(method, endpoint, data)
            print("maybe salesforce secret is outdated?...")

    def update(self, sobjectName: str, idObject: str, fields_to_updated: dict):
        response = {}
        try:
            sobject = SFType(
                sobjectName,
                self.connection.session_id,
                self.connection.sf_instance
            )
            response = sobject.update(
                idObject,
                fields_to_updated,
            )
        except Exception:
            response = {}
        finally:
            return response

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
