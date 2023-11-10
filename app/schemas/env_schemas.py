# baseModel verity the type of data on wich the classes are instanciated
from pydantic import BaseModel


class AppSchema(BaseModel):
    port: int
    host: str
    name_env: str


class SalesForceSchema(BaseModel):
    sf_client_id: str
    sf_client_secret: str
    sf_redirect_uri: str
    sf_login_url: str
    sf_user: str
    sf_pass: str
    sf_password: str
    sf_pass: str
    sf_enviroment: str


class AuthSchema(BaseModel):
    auth_salesforce_api_key: str
