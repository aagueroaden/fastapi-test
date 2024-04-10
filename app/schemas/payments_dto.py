from pydantic import BaseModel, PositiveInt, Field
from datetime import date


class Payment(BaseModel):
    payment_type: str = Field(min_length=1)
    billing_company: str = Field(min_length=1)
    currency1: str = Field(min_length=1)
    amount = float = Field(ge=0)
    numberOfInstallments: PositiveInt
    deferredPaymentDay: str[date]
