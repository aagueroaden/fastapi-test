ADD_ONE_FILE = "Add at least one file of: titulo_bachiller, documento_identidad, foto, solicitud_preconvalidacion, creditos_universidad"


# endpoints
CONTACT_SOBJECT = '/services/data/v53.0/sobjects/Contact/describe/'
FORMULARIO_INSCRIPCION_SOBJECT = '/services/data/v53.0/sobjects/Formulario_Inscripci_n__c/describe/'

# this endpoint returns the same as /services/data/v53.0/sobjects/Contact/describe/
CONTACTS_SERVICE_CITIZENSHIP = '/services/data/v53.0/sobjects/Contact/describe/?fields=hed__Citizenship__c'

# this endpoint returns the same as /services/data/v53.0/sobjects/Contact/describe/
TEST = '/services/data/v53.0/sobjects/Contact/describe/?fields=hed__Citizenship__c&label=Nacionalidad',
