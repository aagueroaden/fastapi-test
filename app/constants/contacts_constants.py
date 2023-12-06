ADD_ONE_FILE = "Add at least one file of: titulo_bachiller, documento_identidad, foto, solicitud_preconvalidacion, creditos_universidad"
GET_COUNTRIES_ERROR_MSG = "there was a problem fetching the countries from salesforce, check endpoint"

# endpoints
CONTACT_SOBJECT = '/services/data/v53.0/sobjects/Contact/describe/'
FORMULARIO_INSCRIPCION_SOBJECT = '/services/data/v53.0/sobjects/Formulario_Inscripci_n__c/describe/'
UPDATE_FORM_INSCRIPTION = '/services/data/v53.0/sobjects/Formulario_Inscripci_n__c/Id_externo__c/'

# this endpoint returns the same as /services/data/v53.0/sobjects/Contact/describe/
CONTACTS_SERVICE_CITIZENSHIP = '/services/data/v53.0/sobjects/Contact/describe/?fields=hed__Citizenship__c'

# this endpoint returns the same as /services/data/v53.0/sobjects/Contact/describe/
TEST = '/services/data/v53.0/sobjects/Contact/describe/?fields=hed__Citizenship__c&label=Nacionalidad',


CONTACT_SELECTS_FIELDS_NAMES = [
    'hed__Gender__c',
    'Tipo_de_documento__c',
    'Grupo_sangu_neo__c',
    'RH__c',
    'Actualmente_se_encuentra_laborando__c',
    'Ocupaci_n_laboral__c',
]

KEYS_OF_CONTACT_SELECTS_FIELDS_NAME = {
    'hed__Gender__c': 'genero',
    'Tipo_de_documento__c': "tipo_de_documento",
    'Grupo_sangu_neo__c': "grupo_sanguineo",
    'RH__c': "rh",
    'Actualmente_se_encuentra_laborando__c': "actualmente_se_encuentra_laborando",
    'Ocupaci_n_laboral__c': "ocupacion_laboral",
    "hed__Citizenship__c": "countries",
}

KEY_OF_FORM_INSCR_SELECTS_FIELDS_NAME = {
    'Estado_civil__c': 'estado_civil',
}

PROGRAM_NAME_ADEN_UNI = 'Aden University'

FORM_INSC_TYPE = 'adenupa'
