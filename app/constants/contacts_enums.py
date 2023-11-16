from enum import Enum


class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    DECLINE_TO_STATE = 'Decline to State'


class HasPreconvalidation(str, Enum):
    SI = 'Sí'
    NO = 'No'


class JobOcupation(str, Enum):
    EMPLEADO = 'Empleado'
    INDEPENDIENTE = 'Independiente (Freelance/Emprendedor)'
    PENSIONADO = 'Pensionado'
    NADA = ''


class DocumentType(str, Enum):
    CEDULA = 'cédula'
    PASAPORTE = 'Pasaporte'
    OTRO = 'otro'


class MaritalStatus(str, Enum):
    SOLTERO = 'Soltero/a'
    CASADO = 'Casado/a'
    DIVORCIADO = 'Divorciado'
    VIUDO = 'Viudo'
    UNION_DE_HECHO = 'Unión de hecho'


class BloodType(str, Enum):
    A = 'A'
    B = 'B'
    O = 'O'
    AB = 'AB'


class RH(str, Enum):
    POS = '(+)'
    NEG = '(-)'
