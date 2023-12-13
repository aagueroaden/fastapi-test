from enum import Enum


class HighSchoolStatus(str, Enum):
    SIN_FINALIZAR = 'Sin finalizar'
    PRONTO_A_FINALIZAR = 'Pronto a finalizar'
    GRADUADO = 'Graduado'
