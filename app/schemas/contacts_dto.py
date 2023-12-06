from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.schemas.contacts_enums import (
    BloodType,
    DocumentType,
    Gender,
    HasPreconvalidation,
    JobOcupation,
    MaritalStatus,
    RH,
)
from fastapi import UploadFile, File


class FormDocumentsDto(BaseModel):
    salesforce_id: str
    student_name: str


# does not work
class FormFilesDto(BaseModel):
    titulo_bachiller: UploadFile = File()
    documento_identidad: UploadFile = File()
    foto: UploadFile = File()
    solicitud_preconvalidacion: UploadFile = File()
    creditos_universidad: UploadFile = File()


class UpdateContactDto(BaseModel):
    """
    Field(min_length=1) avoid receiving empty strings as attributes but nothing more
    the string fields that dosen't have Field() or an Enum, can be empty strings
    """
    name: str
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    birthday: datetime
    gender: Gender
    identification_type: DocumentType
    identification_num: str = Field(min_length=1)
    maritial_status: MaritalStatus
    blood_type: BloodType
    rh: RH
    country_origin: str = Field(min_length=1)
    address_residence: str = Field(min_length=1)
    country_residence: str = Field(min_length=1)
    city_residence: str = Field(min_length=1)
    zip: int | None = Field(default=0)
    high_school_title: str = Field(min_length=1)
    institution_origin: str = Field(min_length=1)
    graduation_year: int = Field(ge=1950, le=3000)
    graduation_country: str = Field(min_length=1)
    country_indication: str = Field(min_length=1)
    email: EmailStr
    alternative_email: EmailStr
    phone: str = Field(min_length=1)
    alternative_phone: str
    attendant_name: str = Field(min_length=1)
    attendant_phone: str = Field(min_length=1)
    facebook: str | None = Field(default='')
    instagram: str | None = Field(default='')
    has_job: bool
    job_ocupation: JobOcupation
    photocopy_title: str
    photo_bg_white: str
    photocopy_document: str = Field(min_length=1)
    has_preconvalidation: HasPreconvalidation
    format_preconvalidation: str
    photocopy_credits: str
