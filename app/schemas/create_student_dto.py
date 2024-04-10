from pydantic import BaseModel, Field, EmailStr
from app.schemas.students_enums import (
    Gender,
    DocumentType,
    MaritalStatus,
    BloodType,
    RH,
    NivelEstudioSecundario,
    PreconvStatus,
    OpportunityType,
    SubmodalityType,
)
from app.schemas.discounts_from_salesforce_dto import DiscountsFromSalesforceDto
from app.schemas.products_from_salesforce_dto import ProductsFromSalesforceDto
from app.schemas.document_from_salesforce_dto import DocumentFromSalesforceDto
from app.schemas.payments_dto import Payment
from datetime import date
from typing import Optional


class CreateStudentDto(BaseModel):

    firstName: str = Field(min_length=1)
    lastName: str = Field(min_length=1)
    gender: Gender
    documentType: DocumentType
    documentNumber: str = Field(min_length=1)
    maritalStatus: MaritalStatus
    bloodType: BloodType
    rh: RH
    country: str = Field(min_length=1)
    state: str = Field(min_length=1)
    street: str = Field(min_length=1)
    zip: str = '111'
    birthdate: date
    phone: str
    email: EmailStr
    leadId: str = Field(min_length=1)
    programId: str = Field(min_length=1)
    programOdooId: Optional[str] = None
    programSisId: Optional[str] = None
    programModality: str = Field(min_length=1)
    programSegment: str
    programBusinessUnit: str
    products: ProductsFromSalesforceDto = None
    sisId: int
    educatId: int
    salesforceContactId: str
    graduationYear: Optional[int] = Field(ge=1949, le=3001, default=None)
    graduationSchool: str
    schoolTitle: Optional[str] = None
    registrationFormDate: date
    enrollmentCohort: str = Field(min_length=1)
    payment: Optional[Payment] = None
    linkDrive: Optional[str] = None
    nivelEstudioSecundario: Optional[NivelEstudioSecundario] = None
    preconvStatus: Optional[PreconvStatus]
    comercial: Optional[EmailStr] = None
    paisProcedencia: Optional[str] = None
    paisResidencia: Optional[str] = None
    opportunityType: Optional[OpportunityType] = None
    submodality: Optional[SubmodalityType]
    documents: Optional[DocumentFromSalesforceDto] = None
    mailingAddress: Optional[str] = None
    discounts: DiscountsFromSalesforceDto
    ifharu: Optional[bool] = None
