from pydantic import BaseModel, Field


class DiscountsFromSalesforceDto(BaseModel):
    discountId: str = Field(min_length=1)
    discountName: str = Field(min_length=1)
    discountRate: int = Field(ge=0)
