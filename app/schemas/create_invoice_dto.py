from pydantic import BaseModel, EmailStr, PositiveInt
from app.schemas.products_from_salesforce_dto import ProductsFromSalesforceDto
from app.schemas.discounts_from_salesforce_dto import DiscountsFromSalesforceDto


class CreateInvoiceDto(BaseModel):
    firstName: str
    lastName: str
    documentNumber: str
    phone: str
    email: EmailStr
    salesforceContactId: str
    leadId: str
    products = ProductsFromSalesforceDto
    comercial: str
    educatId: PositiveInt
    discounts = DiscountsFromSalesforceDto
