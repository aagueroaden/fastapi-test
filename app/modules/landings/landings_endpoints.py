from fastapi import APIRouter, HTTPException, status
from app.modules.landings.landings_service import CreateLandingDto
from dependencies import landing_service


landings_router = APIRouter()


@landings_router.post(path='/landings', tags=['Landings'])
async def create(createLanding: CreateLandingDto):
    try:
        response = landing_service.create(createLanding=createLanding)
        if 'error' in response:
            raise HTTPException(
                status_code=response['status'],
                detail=response['error']
            )
        return {'response_data': response}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected Error: {error}"
        )
