from pydantic import BaseModel, Field, EmailStr, HttpUrl
from app.schemas.landing_enums import HighSchoolStatus


class CreateLandingDto(BaseModel):
    # Field(min_length=1) to avoid sending an empty string
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    particular:  EmailStr
    telefono: str = Field(min_length=1)
    ciudad: str | None = Field(
        description='The city must null or not send this parameter',
        default=None
    )
    pais: str = Field(min_length=1)
    idprodmkt: str = Field(min_length=1)
    programa: str = Field(min_length=1)
    consulta: str | None = None
    utm_campaign: str = Field(min_length=1)
    utm_medium: str = Field(min_length=1)
    utm_source: str = Field(min_length=1)
    anio: int | None = Field(ge=1950, le=3000, default=None)
    mes: int | None = Field(ge=1, le=12, default=None)
    dia: int | None = Field(ge=1, le=31, default=None)  # wow this is really inconsistent!
    nombre_referidor: str | None = None
    apellido_referidor: str | None = None
    particular_referidor: EmailStr | None = None
    url_landing: HttpUrl | None = None
    facebook_lead_id: str | None = Field(min_length=1, default=None)
    facebook_event_id: str | None = Field(min_length=1, default=None)
    facebook_client_ip_address: str | None = Field(min_length=1, default=None)
    facebook_client_user_agent:  str | None = Field(min_length=1, default=None)
    high_school_status: HighSchoolStatus | None = None
    utm_content: str | None = Field(default=None, min_length=1)
    utm_term: str | None = Field(min_length=1, default=None)
    convalidar: bool | None = None
    canal: str | None = Field(min_length=1, default=None)
    origen: str | None = Field(min_length=1, default=None)
    suborigen: str | None = Field(min_length=1, default=None)
    formulario_web_id: str | None = None
    cohorte_inversion: str | None = Field(min_length=1, default=None)
