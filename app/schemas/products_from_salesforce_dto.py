from pydantic import BaseModel, Field, PositiveInt


class ProductsFromSalesforceDto(BaseModel):
    productId: str = Field(min_length=1)
    productName: str = Field(min_length=1)
    productCode: str = Field(min_length=1)
    quantity: PositiveInt
    listPrice: float
    salePrice: float
    totalPrice: float
    standardCredits: int
    dualCredits: int
    discount: float = Field(ge=0)
    credits: PositiveInt
    creditTypeId: int = Field(ge=0, le=20)
