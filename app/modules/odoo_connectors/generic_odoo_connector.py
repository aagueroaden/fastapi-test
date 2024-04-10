from xmlrpc import client
import logging


class GenericOdooAdapter:

    instance = None

    def __init__(self, OdooSchema):
        self.user: str = OdooSchema.user
        self.password: str = OdooSchema.password
        self.url: str = OdooSchema.url
        self.db_name: str = OdooSchema.db_name
        self.common = client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self._login_to_odoo()

    def _login_to_odoo(self):
        self.uid = 0
        try:
            self.uid = self.common.authenticate(
                self.db_name,
                self.user,
                self.password,
                {},
            )
        except Exception as error:
            logging.error(str(error))

        if not self.uid:
            logging.error(f"Error in the login of {self.url}")
        else:
            logging.info(f"Successfull login into {self.url}")

    def execute(self, model, method, *args, **kwargs):
        if not self.uid:
            self._login_to_odoo()

        if not self.uid:
            return {
                'status': 504,
                'error': f"Couldnt connect to Server {self.url}"
            }

        try:
            return self.models.execute_kw(
                self.db_name, self.uid, self.password, model, method, list(args), kwargs)
        except Exception as error:
            logging.error(str(error))
            return {
                'status': 504,
                'error': f"Couldnt execute te action {method} in {self.url}"
            }
