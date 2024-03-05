from app.modules.database.database_aden_forms import AdenForms
from app.modules.salesforce.salesforce_service import SalesForceService
from app.schemas.landing_dto import CreateLandingDto
from datetime import datetime, timedelta
from app.constants.landings_constants import FORMULARIO_WEB_SOBJECT
from fastapi import HTTPException, status
from app.utils.helpers.landings import normalize_the_country


class LandingService:

    def __init__(
            self,
            aden_forms,
            salesforce
    ):
        self._aden_forms: AdenForms = aden_forms
        self._salesforce: SalesForceService = salesforce

    def create(self, createLanding: CreateLandingDto) -> None | object:
        interested = self.findOneInteresadoLanding(createLanding)
        if interested:
            return {
                'status': 400,
                'error': 'El formulario ha sido enviado previamente',
            }

        try:
            # add newInteresadoSalesforce as a backup in aden_forms db
            newInteresadoSalesforce = self._aden_forms.createInteresadoSalesforce(createLanding)
            if not newInteresadoSalesforce:
                print("Couldn't create a registry in aden-forms interesado-salesforce")

            product = self.getProductByMarketingId(createLanding.idprodmkt)
            if not product:
                return {
                    'error': f"No existe el Producto para id de Marketing {createLanding.idprodmkt}",
                    'status': 404
                }

            if not product.get('Asignaci_n_comercial__c'):
                return {
                    'error': f"No existe Asignacion comercial para el producto {product.get('Id')}",
                    'status': 400,
                }

            # fetch Comercial Users in ASC order
            orderAsignations = self._salesforce.executeQuery(
                f"""
                SELECT Id, Asignaci_n_comercial__c, Orden__c, Usuario__c, ltima_asignaci_n__c
                FROM Orden_de_asignaci_n_comercial__c
                WHERE Asignaci_n_comercial__c = '{product.get('Asignaci_n_comercial__c')}'
                ORDER BY Orden__c ASC
                """
            )
            if not orderAsignations:
                return {
                    'error': f"""
                    It dosent exits an Orden De asignacion comercial
                    for the {product.get('Asignaci_n_comercial__c')}
                    using idprodmkt {createLanding.idprodmkt}
                    """,
                    'status': 404,
                }
            comercial_user = self.assignComercialUserToTheLanding(orderAsignations=orderAsignations)
            if not comercial_user:
                return {
                    'error': "Couldn't assignt a commercial to the Landing",
                    'status': 500
                }
            web_form = self.createFormularioWeb(
                createLanding,
                comercial_user,
            )
            if not web_form or not web_form.get('id'):
                return {'error': 'Couldnt create the webform', 'status': 500}
            createLanding.formulario_web_id = web_form.get('id')
            return createLanding

        except HTTPException as h_error:
            print(f"Error at createLanding {h_error}")
            return {'error': str(h_error), 'status': 500}
        except Exception as error:
            return {'error': str(error), 'status': 500}

    def assignComercialUserToTheLanding(self, orderAsignations: list[dict]) -> str:
        """
        Assign the commercial to the Landing where it uses the orderAsignations from SF
        search the user that has the ltima_asignaci_n__c in True, change it to False and the next
        user makes it True
        """
        user = ''
        # if it only exist one user to assing with that idprodmkt
        if len(orderAsignations) == 1:
            orderAsignation = orderAsignations[0]
            user = orderAsignation.get('Usuario__c')
            response = self.updateLastAssignationField(
                order_asignation=orderAsignation,
                ltima_asignaci_n__c=True
            )
            return user
        # if it exist more than one or zero
        seleccionarProximoUsuario = False
        for orderAsignation in orderAsignations:
            if seleccionarProximoUsuario:
                user = orderAsignation.get('Usuario__c')
                response = self.updateLastAssignationField(
                    order_asignation=orderAsignation,
                    ltima_asignaci_n__c=True,
                )
                # exits the for loop when it can assign some user
                break
            if orderAsignation.get('ltima_asignaci_n__c'):
                seleccionarProximoUsuario = True
                response = self.updateLastAssignationField(
                    order_asignation=orderAsignation,
                    ltima_asignaci_n__c=False,
                )
        # if it didnt assign any user
        if not user:
            orderAsignation = orderAsignations[0]
            user = orderAsignation.get('Usuario__c')
            response = self.updateLastAssignationField(
                order_asignation=orderAsignation,
                ltima_asignaci_n__c=True
            )
        return user

    def updateLastAssignationField(
        self,
        order_asignation: dict,
        ltima_asignaci_n__c: bool
    ):
        """
        this object is used as a list to assign work to the "comerciales", where if they have the
        check in true, the next one will be asigned to the next landing call
        """
        id = str(order_asignation.get('Id'))
        data = {
            'ltima_asignaci_n__c': ltima_asignaci_n__c
        }
        response = self._salesforce.update(
            sobjectName="Orden_de_asignaci_n_comercial__c",
            idObject=id,
            fields_to_updated=data,
        )
        return response

    def findOneInteresadoLanding(self, createLanding: CreateLandingDto):
        """
        With the "particular" field in the createLandingDto, search in a cretain range of time
        an email in the "InteresadoSalesforce" table in ADEN_FORMS DB, "email" column MATCH
        """
        subtract_min = 15
        # make the microseconds irrelevant
        current_datetime = datetime.now().replace(microsecond=0)
        past_datetime = current_datetime - timedelta(minutes=subtract_min)
        query_response = None
        query_response = self._aden_forms.findRecentEmails(
            email=createLanding.particular,
            current_datetime=current_datetime,
            past_datetime=past_datetime,
            more_than_one_record=False
        )
        return query_response

    def getProductByMarketingId(self, id: str):
        "return a single product by removing it from the list or it returns nothing"
        product = self._salesforce.executeQuery(
            f"""
            SELECT Description, Id, Asignaci_n_comercial__c
            FROM Product2
            WHERE ID_Marketing__c = '{id}'
            """
        )
        return product[0] if product else product

    def createFormularioWeb(self, createLanding: CreateLandingDto, user=False):
        nombre_referidor = createLanding.nombre_referidor + ' ' + createLanding.apellido_referidor
        data = {
            'Nombre__c': createLanding.nombre,
            'Apellido__c': createLanding.apellido,
            'Email__c': createLanding.particular,
            'Tel_fono__c': createLanding.telefono,
            'Ciudad__c': createLanding.ciudad if createLanding.ciudad else '',
            'Pa_s__c': normalize_the_country(createLanding.pais),
            'Nivel_de_estudios__c': '',
            'C_digo_programa__c': createLanding.idprodmkt,
            'Consulta__c': createLanding.programa + '-' + createLanding.consulta,
            'UTM_Campaign__c': createLanding.utm_campaign,
            'UTM_Medium__c': createLanding.utm_medium,
            'UTM_Source__c': createLanding.utm_source,
            'Fecha_de_nacimiento__c': None,
            'Nombre_Referidor__c': nombre_referidor,
            'Email_Referidor__c': createLanding.particular_referidor,
            'URL_Landing__c': str(createLanding.url_landing),
            'Facebook_Lead_Id__c': createLanding.facebook_lead_id,
            'Facebook_Event_Id__c': createLanding.facebook_event_id,
            'Facebook_Client_IP__c': createLanding.facebook_client_ip_address,
            'Facebook_Client_User_Agent__c': createLanding.facebook_client_user_agent,
            'Estado_finalizacion_colegio_secundario__c': createLanding.high_school_status,
            'UTM_Term__c': createLanding.utm_term,
            'Convalidar__c': createLanding.convalidar,
            'Canal__c': createLanding.canal,
            'Origen__c': createLanding.origen,
            'Suborigen__c': createLanding.suborigen,
            # 'Cohorte_inversion__c': createLanding.cohorte_inversion
        }
        if user:
            data['OwnerId'] = user
            data['Asesor_comercial__c'] = user

        # Birthday date
        if (
            createLanding.anio and createLanding.mes and createLanding.dia
        ):
            anio = str(createLanding.anio)
            mes = str(createLanding.mes)
            dia = str(createLanding.dia)

            data['Fecha_de_nacimiento__c'] = anio + "-" + mes + "-" + dia
        webForm = self._salesforce.requestHTTP(
            method='POST',
            endpoint=FORMULARIO_WEB_SOBJECT,
            data=data,
        )
        return webForm
