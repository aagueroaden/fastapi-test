from pydantic import BaseModel, EmailStr, Field
from datetime import date
from app.constants.contacts_enums import (
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
    i dont know it this trully works, some enums have diferent keys that the nest.js enums,
    those accepts strings as keys, the python enums dont
    """
    name: str
    first_name: str
    last_name: str
    birthday: date
    gender: Gender
    identification_type: DocumentType
    identification_num: str
    maritial_status: MaritalStatus
    blood_type: BloodType
    rh: RH
    country_origin: str
    address_residence: str
    country_residence: str
    city_residence: str
    zip: int | None = Field(default=None)
    high_school_title: str
    institution_origin: str
    graduation_year: int = Field(ge=1950, le=3000)
    graduation_country: str
    country_indication: str
    email: EmailStr
    alternative_email: str
    phone: str
    alternative_phone: str
    attendant_name: str
    attendant_phone: str
    facebook: str | None = Field(default=None)
    instagram: str | None = Field(default=None)
    has_job: bool
    job_ocupation: JobOcupation
    photocopy_title: str
    photo_bg_white: str
    photocopy_document: str
    has_preconvalidation: HasPreconvalidation
    format_preconvalidation: str
    photocopy_credits: str
