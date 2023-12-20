from app.modules.salesforce.salesforce_service import SalesForceService
from app.modules.gdrive.gdrive_service import GoogleDriveService
from app.schemas.env_schemas import ContactsSchema
from app.constants.contacts_constants import (
    CONTACTS_SERVICE_CITIZENSHIP,
    CONTACT_SOBJECT,
    FORMULARIO_INSCRIPCION_SOBJECT,
    CONTACT_SELECTS_FIELDS_NAMES,
    KEYS_OF_CONTACT_SELECTS_FIELDS_NAME,
    KEY_OF_FORM_INSCR_SELECTS_FIELDS_NAME,
    PROGRAM_NAME_ADEN_UNI,
    FORM_INSC_TYPE,
    GET_COUNTRIES_ERROR_MSG,
)

from fastapi import UploadFile, HTTPException, status
from typing import List
import base64
from app.utils.helpers.contacts import getNameAndFields, sliceFullName
from app.utils.salesforce.oportunity_map import mappedPaymentsType
from app.schemas.contacts_enums import EnrollmentStatus
from app.schemas.contacts_dto import UpdateContactDto


class ContactsService:

    def __init__(
            self,
            contacts_settings: ContactsSchema,
            google_drive,
            salesforce
    ) -> None:
        self._gdriveService: GoogleDriveService = google_drive
        self._salesforce: SalesForceService = salesforce
        self.baseUrl = contacts_settings.url_form

    def uploadDocumentationDrive(
            self,
            salesforce_id: str,
            student_name: str,
            files: List[UploadFile],
    ):
        response = []
        folderName = salesforce_id + " - " + student_name
        folderId = self._gdriveService.createFolder(folderName=folderName)

        if not folderId:
            return [{'error': 'failed to create the folder in google drive'}]

        for file in files:
            # """it will upload the file one at the time, maybe make it multiprosesing?"""
            response.append(self._gdriveService.uploadFile(file=file, folderId=folderId))
        return response

    def generateLinkForm(self, id: str):
        id_to_ascii = id.encode("ascii")
        hash = base64.b64encode((id_to_ascii))
        hash_to_str = hash.decode("utf-8")
        return {
            "hash": hash_to_str,
            "base_url": self.baseUrl,
            "link": self.baseUrl + "/" + hash_to_str
        }

    def getCountries(self):
        response: dict = {}
        try:
            request = self._salesforce.requestHTTP(
                method='GET',
                endpoint=CONTACTS_SERVICE_CITIZENSHIP,
                data=''
            )
            if "fields" not in request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=GET_COUNTRIES_ERROR_MSG
                )
            fieldsContact: list = request.get("fields")
            for item in fieldsContact:
                if item['name'] == "hed__Citizenship__c":
                    fieldName, fieldValue = getNameAndFields(
                        name="hed__Citizenship__c",
                        item=item,
                        names_formatted=KEYS_OF_CONTACT_SELECTS_FIELDS_NAME,
                    )
                    response[fieldName] = fieldValue
                    # if already has all the data that it needs, stop looping
                    break

        except HTTPException as error:
            response = {'error': error}

        finally:
            return response

    def getSelectsField(self):
        response: dict = {}
        try:
            contact = self._salesforce.requestHTTP(
                method='GET',
                endpoint=CONTACT_SOBJECT,
                data=''
            )
            counter: int = 1
            fieldsContact: list = contact.get('fields')
            for item in fieldsContact:
                if item['name'] in CONTACT_SELECTS_FIELDS_NAMES:
                    fieldName, fieldValue = getNameAndFields(
                        name=item['name'],
                        item=item,
                        names_formatted=KEYS_OF_CONTACT_SELECTS_FIELDS_NAME
                    )
                    response[fieldName] = fieldValue

                    # if already has all the data that it needs, stop looping
                    counter += 1
                    if counter == len(KEYS_OF_CONTACT_SELECTS_FIELDS_NAME):
                        break

            form = self._salesforce.requestHTTP(
                method='GET',
                endpoint=FORMULARIO_INSCRIPCION_SOBJECT,
                data=''
            )

            fieldsFormInscrip: list = form.get("fields")
            for item in fieldsFormInscrip:
                if item['name'] == 'Estado_civil__c':
                    fieldName, fieldValue = getNameAndFields(
                        name='Estado_civil__c',
                        item=item,
                        names_formatted=KEY_OF_FORM_INSCR_SELECTS_FIELDS_NAME,
                    )
                    response[fieldName] = fieldValue
                    # if already has all the data that it needs, stop looping
                    break

        except Exception as error:
            response = {'error': error}

        finally:
            return response

    def getFormInscription(self, hashId: str, leadId: str) -> dict:
        try:
            # search the opportunity
            lead = self._salesforce.executeQuery(
                f"""
                SELECT AccountId, Programa_acad_mico__c
                FROM Opportunity
                WHERE Id = '{leadId}'
                """
            )

            # if it didn't find anyhing with id= leadId
            if not lead:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Opportunity not found for id {leadId}"
                )

            # use the ONLY registry that SHOULD EXIST
            lead: dict = lead[0]

            # search the account associated to the opp of id leadId
            account = self._salesforce.executeQuery(
                f"""
                SELECT hed__Primary_Contact__c
                FROM Account
                WHERE Id = '{lead["AccountId"]}'
                """
            )

            # if it didn't find anything in that account
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            # use the ONLY registry that SHOULD EXIST
            account: dict = account[0]

            # search the data of the account primary contact
            contact = self._salesforce.executeQuery(
                f"""
                SELECT Id, FirstName, LastName, Name, Email, hed__Country_of_Origin__c, Birthdate,
                    hed__Gender__c, Tipo_de_documento__c, Numero_de_documento__c,
                    Grupo_sangu_neo__c, RH__c, hed__Current_Address__c,
                    Institucion_de_procedencia__c, hed__AlternateEmail__c, Phone, OtherPhone,
                    Nombre_del_acudiente__c, Tel_particular_del_acudiente__c,
                    Usuario_de_Instagram__c, Usuario_de_Facebook__c,
                    Actualmente_se_encuentra_laborando__c, Ocupaci_n_laboral__c, Estado_civil__c,
                    MailingStreet, MailingCity, MailingState, MailingPostalCode
                FROM Contact
                WHERE Id = '{account["hed__Primary_Contact__c"]}'
                """
            )

            # if it didn't find any contact with that account contact
            if not contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Contact not found, error fetching salesforce contact"
                )

            # use the ONLY registry that SHOULD EXIST
            contact: dict = contact[0]

            # check if it has a defined program name, if not, default to aden university
            if lead["Programa_acad_mico__c"]:
                program = self._salesforce.executeQuery(
                    f"""
                    SELECT Name
                    FROM Account
                    WHERE Id = '{lead["Programa_acad_mico__c"]}'
                    """
                )
                program_name = program[0]["Name"] if program else PROGRAM_NAME_ADEN_UNI

            payments = self._salesforce.executeQuery(
                f"""
                SELECT Id, Cantidad_de_cuotas__c, CreatedById, Divisa__c, Forma_de_pago__c,
                    Importe__c, Name, Obtener_link_Forma_de_pago__c, Oportunidad__c,
                    Respuesta_Hash__c, Respuesta_Link__c, Respuesta_Tipo__c,
                    Total_de_Formas_de_pago__c, LastModifiedById
                FROM Forma_de_pago__c
                WHERE Oportunidad__c = '{leadId}'
                AND Forma_de_pago__c = 'Online - Aden Checkout'
                """
            )

            # rename the keys of all the payments
            arrPayments: list = [
                mappedPaymentsType(dict(payment)) for payment in payments
            ] if payments else []

            # change the value of installment_amount if posible
            for payment in arrPayments:
                if payment['qty_installments'] > 0:
                    payment[
                        'installment_amount'
                    ]: float = payment['total_amount'] / payment['qty_installments']

            form_inscription = self._salesforce.executeQuery(
                f"""
                SELECT Name
                FROM Formulario_Inscripci_n__c
                WHERE Oportunidad__c = '{leadId}'
                """
            )

            # inscription is completed
            if form_inscription:
                return {
                    'id': hashId,
                    'contact_salesforce_id': contact['Id'],
                    'type': FORM_INSC_TYPE,
                    'enrrollment_status': EnrollmentStatus.COMPLETE,
                    'program': program_name,
                    'arr_payments': arrPayments
                }

            # inscription isn't completed, is pending
            else:
                return {
                    'id': hashId,
                    'contact_salesforce_id': contact['Id'],
                    'type': FORM_INSC_TYPE,
                    'enrrollment_status': EnrollmentStatus.PENDING,
                    'program': program_name,
                    'personal_data': {
                        'name': contact['Name'],
                        'first_name': contact['FirstName'],
                        'last_name': contact['LastName'],
                        'birthday': contact['Birthdate'],
                        'gender': contact['hed__Gender__c'],
                        'identification_type': contact['Tipo_de_documento__c'],
                        'identification_num': contact['Numero_de_documento__c'],
                        'maritial_status': contact['Estado_civil__c'],
                        'blood_type': contact['Grupo_sangu_neo__c'],
                        'rh': contact['RH__c'],
                        'country_origin': contact['hed__Country_of_Origin__c'],
                        'address_residence': contact['MailingStreet'],
                        # same key as country_origin... why do this?
                        'country_residence': contact['hed__Country_of_Origin__c'],
                        'city_residence': contact['MailingCity'],
                        'zip': contact['MailingPostalCode'],
                    },
                    'academic_information': {
                        'institution_origin': contact['Institucion_de_procedencia__c'],
                        'high_school_title': contact.get('T_tulo_recibido__c'),
                        # high_school_title, graduation_year, graduation_country and
                        # country_indication:
                        # these keys does not exist in the "Contact" Sobject, they exist in the
                        # "Formulario_Inscripci_n__c", but here(the else statement) only access
                        # if the form inscription is not completed, hence, the opportunity does
                        # not exist in Formulario_Inscripci_n__c sobject, they always be null
                        # 'high_school_title': contact.get('Titulo_del_colegio_recibido__c'),
                        'graduation_year': contact.get('A_o_de_graduaci_n__c'),
                        'graduation_country': contact.get('Pa_s_de_graduaci_n__c'),
                        'country_indication': contact.get('Indicativo_del_pa_s__c'),
                    },
                    'contact_information': {
                        'email': contact['Email'],
                        'alternative_email': contact['hed__AlternateEmail__c'],
                        'phone': contact['Phone'],
                        'alternative_phone': contact['OtherPhone'],
                        'attendant_name': contact['Nombre_del_acudiente__c'],
                        'attendant_phone': contact['Tel_particular_del_acudiente__c'],
                        'instagram': contact['Usuario_de_Instagram__c'],
                        'facebook': contact['Usuario_de_Facebook__c'],
                    },
                    'job_information': {
                        'has_job': contact['Actualmente_se_encuentra_laborando__c'],
                        'job_ocupation': contact['Ocupaci_n_laboral__c'],
                    },
                    'documentation': {
                        'photocopy_title': '',
                        'photoBgWhite': '',
                        'photocopy_document': '',
                        'has_preconvalidation': '',
                        'format_preconvalidation': '',
                        'photocopy_credits': '',
                    },
                    'arr_payments': arrPayments
                }

        except HTTPException as error:
            print(f"error at getFormInscription {error}")
            return {'error': error}

        # finally:
        #     return response

    def updateformInscription(self, formId: str, contactToUpdate: UpdateContactDto):
        # if you pass the hashedId directly, need to be decoded
        # try:
        #    formId = base64.b64decode(formId).decode("utf-8")
        # except Exception:
        #    raise {'error': f'The hashId provided: {formId} , is an invalid hashId'}
        try:
            contactToUpdate.zip = str(contactToUpdate.zip) if contactToUpdate.zip else None
            has_job = 'Sí' if contactToUpdate.has_job else 'No'
            attendantFirstName, attendantLastName = sliceFullName(contactToUpdate.attendant_name)
            timeInISOFormat = str(contactToUpdate.birthday.isoformat()).replace('+00:00', 'Z')

            data: dict = {
                'Nombre__c': contactToUpdate.first_name,
                'Apellidos__c': contactToUpdate.last_name,
                'Fecha_de_nacimiento__c': timeInISOFormat,
                'G_nero__c': contactToUpdate.gender.value,
                'Tipo_de_documento_de_identidad__c': contactToUpdate.identification_type.value,
                'N_mero_de_documento_de_identidad__c': contactToUpdate.identification_num,
                'Estado_civil__c': contactToUpdate.maritial_status.value,
                'Grupo_sangu_neo__c': contactToUpdate.blood_type.value,
                'RH__c': contactToUpdate.rh.value,
                'Pais_de_procedencia__c': contactToUpdate.country_origin,
                'Direcci_n_de_residencia__c': contactToUpdate.address_residence,
                'Ciudad_de_residencia__c': contactToUpdate.city_residence,
                'Pa_s_de_residencia__c': contactToUpdate.country_residence,
                'C_digo_postal__c': contactToUpdate.zip,
                'Titulo_del_colegio_recibido__c': contactToUpdate.high_school_title,
                'Instituci_n_de_procedencia_texto__c': contactToUpdate.institution_origin,
                'A_o_de_graduaci_n__c': contactToUpdate.graduation_year,
                'Pa_s_de_graduaci_n__c': contactToUpdate.graduation_country,
                'Indicativo_del_pa_s__c': contactToUpdate.country_indication,
                'Correo_electr_nico_Personal__c': contactToUpdate.email,
                'Correo_electr_nico_Alterno__c': contactToUpdate.alternative_email,
                'Tel_fono_particular__c': contactToUpdate.phone,
                'Telef_no_Alterno__c': contactToUpdate.alternative_phone,

                'Nombre_del_acudiente__c': attendantFirstName,  # variable
                'Apellido_del_acudiente__c': attendantLastName,  # variable

                'Tel_particular_del_acudiente__c': contactToUpdate.attendant_phone,
                'Usuario_de_Instagram__c': contactToUpdate.instagram,
                'Usuario_de_Facebook__c': contactToUpdate.facebook,

                'Actualmente_se_encuentra_laborando__c': has_job,  # variable

                'Ocupaci_n_laboral__c': contactToUpdate.job_ocupation.value,
                'Hace_preconvalidaci_n__c': contactToUpdate.has_preconvalidation.value,

                # these fields wont store files, it will store the same value,
                # an url to a google drive folder. "Fotocopia_de_documento_de_identidad__c"
                # "Foto_fondo_blanco__c" and "Fotocopia_de_Titulo_de_Bachiller__c" are most used
                'Fotocopia_de_Titulo_de_Bachiller__c': contactToUpdate.photocopy_title,  # FILE?
                'Foto_fondo_blanco__c': contactToUpdate.photo_bg_white,  # FILE?
                'Fotocopia_de_documento_de_identidad__c':
                    contactToUpdate.photocopy_document,  # FILE?
                'Formato_de_solicitud_de_preconvalidaci_n__c':
                    contactToUpdate.format_preconvalidation,  # FILE?
                'Fotocopia_de_creditos_de_la_universidad__c':
                    contactToUpdate.photocopy_credits,  # FILE?

                'Acepta_t_rminos_y_condiciones__c': True,  # hardcoded
                'Acepta_pol_ticas__c': True,  # hardcoded
                'Acepta_el_contrato_de_estudios__c': True,  # hardcoded
            }
            response = self._salesforce.update(
                sobjectName='Formulario_Inscripci_n__c',
                idObject=formId,
                fields_to_updated=data
            )
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Could not update the Sobject {formId}, an error in the data or Id'
                )
            else:
                return data
        except HTTPException as error:
            return {'error': error}

    def decodeHashedIdtoSfId(self, hashId) -> dict:
        """
        return the decoded Id as a string or a error in dict format
        """
        try:
            Id = base64.b64decode(hashId).decode("utf-8")
            return {'id': Id}
        except Exception:
            return {'error': f'The hashId provided: {hashId} , is an invalid hashId'}
