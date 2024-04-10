from enum import Enum


class AcademicLevel(str, Enum):
    BASICO = 'basico'
    MEDIO = 'medio'


class BloodGroup(str, Enum):
    A_POS = 'A+'
    A_NEG = 'A-'
    B_POS = 'B+'
    B_NEG = 'B-'
    O_POS = 'O+'
    O_NEG = 'O-'
    AB_POS = 'AB+'
    AB_NEG = 'AB-'


class BloodType(str, Enum):
    A = 'A'
    B = 'B'
    Oo = 'O'
    AB = 'AB'


class DocumentType(str, Enum):
    CEDULA = 'cédula'
    PASAPORTE = 'Pasaporte'
    OTRO = 'otro'


class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    DECLINE_TO_STATE = 'Decline to State'


class JobType(str, Enum):
    EMPLEADO = 'Empleado'
    INDEPENDIENTE = 'Independiente (Freelance/Empleador)'
    PENSIONADO = 'Pensionado'


class MaritalStatus(str, Enum):
    SOLTERO = 'Soltero/a'
    CASADO = 'Casado/a'
    DIVORCIADO = 'Divorciado'
    VIUDO = 'Viudo'
    UNION_DE_HECHO = 'Unión de hecho'


class NivelEstudioSecundario(str, Enum):
    BASICO = 'Básico'
    MEDIO = 'Medio'


class OpportunityType(str, Enum):
    GRADO = 'Grado'
    GRADO_REMATRICULA = 'Grado - Rematricula'


class PreconvStatus(str, Enum):
    SI = 'Sí'
    NO = 'No'


class RH(str, Enum):
    POS = '(+)'
    NEG = '(-)'


class SubmodalityType(str, Enum):
    FAST_TRACK = 'FastTrack'
    REGULAR_TRACK = 'RegularTrack'
    NUEVO_REGULAR = 'NuevoRegular'
    NULL = 'null'
