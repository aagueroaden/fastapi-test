from app.modules.salesforce.salesforce_service import SalesForceService
from app.utils.salesforce.oportunity_map import mappedOportunityById
from app.constants.opportunity_constants import (
    OPPORTUNITY_SERVICE_ENDPOINT,
    CONTACT_SERVICE_ENDPOINT,
    USER_SERVICE_ENDPOINT,
)
from fastapi import HTTPException, status


class OpportunityService:

    def __init__(self, salesforce: SalesForceService):
        self._salesforce = salesforce

    def find0ne(self, id: str):
        """
        if it fails to find the opportunity returns a 404, but if
        it does not find owner or contacto_principal__c it will not raise 404
        ¡?
        """
        response = {}
        try:
            opportunity = self._salesforce.requestHTTP(
                method='GET',
                endpoint=OPPORTUNITY_SERVICE_ENDPOINT + id,
                data=''
            )
            if not opportunity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Opportunity {id}, not found',
                )

            owner = self._salesforce.requestHTTP(
                method='GET',
                endpoint=USER_SERVICE_ENDPOINT + opportunity["OwnerId"],
                data=''
            )
            if not owner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'OwnerId for Opportunity {id}, not found',
                )

            contact = self._salesforce.requestHTTP(
                method='GET',
                endpoint=CONTACT_SERVICE_ENDPOINT + opportunity['Contacto_principal__c'],
                data='',
            )

            if not contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Contacto_principal__c for Opportunity {id}, not found',
                )

            comercial_for_mapping = {
                'email': owner["Email"],
                'name': owner["Name"],
            }

            contact_data_for_mapping = {
                'email': contact['Email'],
                'lastName': contact['LastName'],
                'firstName': contact['FirstName'],
                'name': contact['Name'],
                'phone': contact['Phone'],
                'documentNumber': contact['Numero_de_documento__c']
            }

            response = mappedOportunityById(opportunity)
            response['comercial'] = comercial_for_mapping
            response['contact'] = contact_data_for_mapping
            # response = mappedOpportunity

        except HTTPException as e:
            # response = e
            response = {'error': e}
        finally:
            return response

    # not used
    def findOneBySisId(self, id: str):
        opportunity = self._salesforce.requestHTTP(
            method='GET',
            endpoint=OPPORTUNITY_SERVICE_ENDPOINT + id,
            data=''
        )
        if not opportunity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Opportunity not found',
            )

    def findOpportunityAmt(self, id: str):
        response: dict = {}
        try:
            opportunity = self._salesforce.requestHTTP(
                method='GET',
                endpoint=OPPORTUNITY_SERVICE_ENDPOINT + id,
                data=''
            )

            if not opportunity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Opportunity {id}, not found',
                )

            mappedOpportunity = mappedOportunityById(opportunity)
            response = {'amount': False} if not mappedOpportunity['amount'] else {'amount': mappedOpportunity['amount']}

        except HTTPException as e:
            # response = e
            response = {'error': e}
        finally:
            return response
