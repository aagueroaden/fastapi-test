from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.landings.landings_service import LandingService
from app.modules.opportunities.opportunities_service import OpportunityService
from app.modules.database.database_aden_forms import AdenForms
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.modules.contacts.contacts_service import ContactsService
from app.schemas.env_schemas import (
    AppSchema,
    SalesForceSchema,
    GoogleDriveSchema,
    ContactsSchema,
    MysqlAdenFormsSchema
)
import os
import sys

app_settings = AppSchema(
    port=int(os.environ.get('APP_PORT')),
    host=os.environ.get('APP_HOST'),
    name_env=os.environ.get('NAME_ENV')
)

salesforce_settings = SalesForceSchema(
    sf_client_id=os.environ.get('SF_CLIENT_ID'),
    sf_client_secret=os.environ.get('SF_CLIENT_SECRET'),
    sf_redirect_uri=os.environ.get('SF_REDIRECT_URI'),
    sf_login_url=os.environ.get('SF_LOGIN_URL'),
    sf_user=os.environ.get('SF_USER'),
    sf_pass=os.environ.get('SF_PASS'),
    sf_password=os.environ.get('SF_PASSWORD'),
    sf_enviroment=os.environ.get('NAME_ENV')
)

gdrive_settings = GoogleDriveSchema(
    gd_scopes_url=[os.environ.get('DRIVE_SCOPE_URL')],
    gd_folder_id=os.environ.get('DRIVE_FOLDER_ID'),
    gd_client_email=os.environ.get('DRIVE_CLIENT_EMAIL'),
    # gd_private_key=os.environ.get('DRIVE_PRIVATE_KEY'),
)

contacts_settings = ContactsSchema(
    url_form=os.environ.get('URL_FORM')
)

mysql_aden_form_settings = MysqlAdenFormsSchema(
    mysql_host=os.environ.get('MYSQL_HOST'),
    mysql_port=int(os.environ.get('MYSQL_PORT')),
    mysql_user=os.environ.get('MYSQL_USER'),
    mysql_password=os.environ.get('MYSQL_PASSWORD'),
    mysql_db=os.environ.get('MYSQL_DB')
)

# instance of modules
# could not connect to the salesforce instance, exit program
salesforce_service = SalesForceService(salesforce_settings)
if not salesforce_service.connection:
    sys.exit()

# Opportunity instances
opportunity_service = OpportunityService(salesforce_service)

# Contact instaces
google_drive_service = GoogleDriveService(gdrive_settings)
contacts_service = ContactsService(
    contacts_settings=contacts_settings,
    google_drive=google_drive_service,
    salesforce=salesforce_service
)

# Landing instances
aden_forms_service = AdenForms(mysql_aden_form_settings)
landing_service = LandingService(
    aden_forms=aden_forms_service,
    salesforce=salesforce_service
)
