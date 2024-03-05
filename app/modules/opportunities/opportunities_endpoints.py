from dependencies import opportunity_service
from fastapi import APIRouter

opportunities_router = APIRouter()


@opportunities_router.get(path="/oportunities/{id}", tags=['Opportunity'])
async def oportunities(id: str):
    opportunity = opportunity_service.find0ne(id=id)
    if 'error' in opportunity:
        raise opportunity['error']
    else:
        return {"response_data": opportunity}


@opportunities_router.get(path="/oportunities/amount/{id}", tags=['Opportunity'])
async def opportunity_amount(id: str):
    opportunity = opportunity_service.findOpportunityAmt(id=id)
    if 'error' in opportunity:
        raise opportunity['error']
    else:
        return {"response_data": opportunity}
