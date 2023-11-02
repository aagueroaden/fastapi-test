import os
import sys
from dotenv import load_dotenv
import argparse
import dataclasses


@dataclasses.dataclass
class AppSettings:
    port: int
    host: str


@dataclasses.dataclass
class SalesForceSettings:
    sf_client_id: str
    sf_client_secret: str
    sf_redirect_uri: str
    sf_login_url: str
    sf_user: str
    sf_pass: str
    sf_password: str


@dataclasses.dataclass
class AuthSettings:
    auth_salesforce_api_key: str


def envArgumentValidation():
    parser = argparse.ArgumentParser(
        description="""
            Start the APP with .env variables [-h HELP] [-e ENV]
            specify the enviroment that the app will run
        """
    )
    parser.add_argument('-e', '--enviroment',
                        metavar='ENVIROMENT',
                        type=str,
                        required=True,
                        help='-e test for the load of the test env | -e prod for production | -e dev for development'
                        )
    args = parser.parse_args()
    enviroment = args.enviroment
    if enviroment not in ['test', 'prod', 'dev']:
        sys.stdout.write('You need to specify a valid enviroment, check the -h for more info')
        sys.exit()
    else:
        return enviroment


def getEnvSettings(env):
    options = {
        'test': 'stage.test.env',
        'prod': 'stage.production.env',
        'dev': 'stage.development.env'
    }
    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), options[env])
    except Exception as dotenv_path_error:
        print(f"cannot load the .env file, error= {dotenv_path_error}")
    try:
        load_dotenv(dotenv_path)

        # proyect
        PORT = int(os.environ.get('PORT'))
        HOST = os.environ.get('HOST')

        # salesforce
        SF_CLIENT_ID = os.environ.get('SF_CLIENT_ID')
        SF_CLIENT_SECRET = os.environ.get('SF_CLIENT_SECRET')
        SF_REDIRECT_URI = os.environ.get('SF_REDIRECT_URI')
        SF_LOGIN_URL = os.environ.get('SF_LOGIN_URL')
        SF_USER = os.environ.get('SF_USER')
        SF_PASS = os.environ.get('SF_PASS')
        SF_PASSWORD = os.environ.get('SF_PASSWORD')

        # AUTH API KEYS
        AUTH_SALESFORCE_API_KEY = os.environ.get('AUTH_SALESFORCE_API_KEY')

        app_settings = AppSettings(
            port=PORT,
            host=HOST,
        )
        salesforce_settings = SalesForceSettings(
            sf_client_id=SF_CLIENT_ID,
            sf_client_secret=SF_CLIENT_SECRET,
            sf_redirect_uri=SF_REDIRECT_URI,
            sf_login_url=SF_LOGIN_URL,
            sf_user=SF_USER,
            sf_pass=SF_PASS,
            sf_password=SF_PASSWORD,
        )
        auth_settings = AuthSettings(
            auth_salesforce_api_key=AUTH_SALESFORCE_API_KEY
        )
        return app_settings, salesforce_settings, auth_settings
    except Exception as load_dotenv_error:
        print(f" error creating the settings object: {load_dotenv_error}")

