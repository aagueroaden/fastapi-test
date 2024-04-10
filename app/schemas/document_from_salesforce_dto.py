from pydantic import BaseModel
from typing import Optional


class DocumentFromSalesforceDto(BaseModel):
    creditos_universidad: Optional[str] = None
    documento_identidad: Optional[str] = None
    titulo_bachiller: Optional[str] = None
    foto: Optional[str] = None
    solicitud_preconvalidacion: Optional[str] = None
