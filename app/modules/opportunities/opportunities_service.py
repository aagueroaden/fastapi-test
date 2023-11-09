from app.modules.salesforce.salesforce_service import SalesForceService
from fastapi import HTTPException, status
from app.utils.salesforce.oportunity_map import mappedOportunityById


class OpportunityService:

    def __init__(self, salesforce: SalesForceService):
        self.salesforce = salesforce

    def find0ne(self, id: str):
        try:
            opportunity = self.salesforce.requestHTTP(
                method='GET',
                endpoint='/services/data/v53.0/sobjects/Opportunity/' + id,
                data=''
            )
            if not opportunity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Opportunity not found')

            owner = self.salesforce.requestHTTP(
                method='GET',
                endpoint='/services/data/v53.0/sobjects/User/' + opportunity["OwnerId"],
                data=''
            )

            comercial_for_mapping = {
                'email': owner["Email"],
                'name': owner["Name"],
            }

            contact = self.salesforce.requestHTTP(
                method='GET',
                endpoint='/services/data/v53.0/sobjects/Contact/' + opportunity['Contacto_principal__c'],
                data='',
            )

            contact_data_for_mapping = {
                'email': contact['Email'],
                'lastName': contact['LastName'],
                'firstName': contact['FirstName'],
                'name': contact['Name'],
                'phone': contact['Phone'],
                'documentNumber': contact['Numero_de_documento__c']
            }

            mappedOpportunity = mappedOportunityById(opportunity)
            mappedOpportunity['comercial'] = comercial_for_mapping
            mappedOpportunity['contact'] = contact_data_for_mapping
            return mappedOpportunity

        except HTTPException:
            pass
