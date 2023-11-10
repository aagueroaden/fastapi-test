from app.utils.helpers.mapped_object import mappedObject
from app.constants.salesforce_constants import BASE_SALESFORCE_OBJ_MAP


def mappedOportunityById(data: dict):
    return mappedObject(
        dict_base=BASE_SALESFORCE_OBJ_MAP,
        data=data
    )
