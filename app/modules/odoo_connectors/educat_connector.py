from app.schemas.env_schemas import OdooSchema
from app.modules.odoo_connectors.generic_odoo_connector import GenericOdooAdapter


class EducatAdapter(GenericOdooAdapter):

    def __init__(self, OdooSettings: OdooSchema):
        super().__init__(OdooSchema=OdooSettings)
