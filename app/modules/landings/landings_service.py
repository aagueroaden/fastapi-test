from app.modules.database.database_aden_forms import AdenForms
from app.modules.salesforce.salesforce_service import SalesForceService
from app.schemas.landing_dto import CreateLandingDto
from datetime import datetime, timedelta


class LandingService:

    def __init__(
            self,
            aden_forms,
            salesforce
    ):
        self._aden_forms: AdenForms = aden_forms
        self._salesforce: SalesForceService = salesforce

    def create(self, createLanding: CreateLandingDto) -> None | object:
        return self.findOneInteresadoLanding(createLanding)

    def findOneInteresadoLanding(self, createLanding: CreateLandingDto):
        """
        With the "particular" field in the createLandingDto, search in a cretain range of time
        an email in the "InteresadoSalesforce" table in ADEN_FORMS DB, "email" column MATCH
        """
        subtract_min = 15
        current_datetime = datetime.now().replace(microsecond=0)
        past_datetime = current_datetime - timedelta(minutes=subtract_min)
        query_response = None
        query_response = self._aden_forms.findRecentEmails(
            email=createLanding.particular,
            current_datetime=current_datetime,
            past_datetime=past_datetime,
            more_than_one_record=False
        ).first()
        return query_response
