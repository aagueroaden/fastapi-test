import os
import sys
from dotenv import load_dotenv
import argparse
from app.schemas.env_schemas import AppSchema, SalesForceSchema, AuthSchema
from typing import List
from app.constants.settings_constants import envOptionsPaths


def envArgumentValidation() -> str | SystemExit:
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
                        help="""-e test for the load of the test env |
                                -e prod for production |
                                -e dev for development |
                        """
                        )
    args = parser.parse_args()
    enviroment = args.enviroment
    if enviroment not in envOptionsPaths:
        sys.stdout.write('You need to specify a valid enviroment, check the -h for more info')
        sys.exit()
    else:
        return envOptionsPaths[enviroment], enviroment


def getEnvSettings(env: str, name_env: str) -> List | SystemExit:

    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), env)
        if not os.path.exists(dotenv_path):
            print(f"enviroment file in {dotenv_path} does not exist")
            raise Exception

    except Exception as dotenv_path_error:
        print(f"cannot load the .env file, error= {dotenv_path_error}")
        sys.exit()

    try:
        load_dotenv(dotenv_path)

        app_settings = AppSchema(
            port=int(os.environ.get('APP_PORT')),
            host=os.environ.get('APP_HOST'),
            name_env=name_env
        )

        salesforce_settings = SalesForceSchema(
            sf_client_id=os.environ.get('SF_CLIENT_ID'),
            sf_client_secret=os.environ.get('SF_CLIENT_SECRET'),
            sf_redirect_uri=os.environ.get('SF_REDIRECT_URI'),
            sf_login_url=os.environ.get('SF_LOGIN_URL'),
            sf_user=os.environ.get('SF_USER'),
            sf_pass=os.environ.get('SF_PASS'),
            sf_password=os.environ.get('SF_PASSWORD'),
            sf_enviroment=name_env
        )

        auth_settings = AuthSchema(
            auth_salesforce_api_key=os.environ.get('AUTH_SALESFORCE_API_KEY')
        )

        return app_settings, salesforce_settings, auth_settings

    except Exception as load_dotenv_error:
        print(f" error creating the settings object: {load_dotenv_error}")
        sys.exit()
