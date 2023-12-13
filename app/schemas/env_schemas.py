# baseModel vary the type of data on wich the classes are instanciated
from pydantic import BaseModel, Field


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


class GoogleDriveSchema(BaseModel):
    gd_scopes_url: list
    gd_folder_id: str
    gd_client_email: str
    # gd_private_key: str


class AuthSchema(BaseModel):
    auth_salesforce_api_key: str


class ContactsSchema(BaseModel):
    url_form: str


class MysqlAdenFormsSchema(BaseModel):
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str = Field(default='')
    mysql_db: str
