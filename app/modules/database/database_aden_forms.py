from app.schemas.env_schemas import MysqlAdenFormsSchema
from sqlalchemy import (
    create_engine,
    Engine,
    and_,
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
)
from abc import ABC, abstractmethod
from datetime import datetime
from app.modules.landings.interesado_salesforce_entity import InteresadoSalesforce
from app.schemas.landing_dto import CreateLandingDto


class Database(ABC):

    def __init__(
        self,
        database_user,
        database_password,
        database_name,
        database_host,
        database_port
    ):
        self.user = database_user
        self.password = database_password
        self.database_name = database_name
        self.host = database_host
        self.port = database_port
        self.engine: Engine = None

    @abstractmethod
    def get_connection(self):
        pass


class AdenForms:

    def __init__(self, adenform_settings: MysqlAdenFormsSchema):
        self.user = adenform_settings.mysql_user
        self.password = adenform_settings.mysql_password
        self.database = adenform_settings.mysql_db
        self.host = adenform_settings.mysql_host
        self.port = adenform_settings.mysql_port
        self.db_type = 'mysql+pymysql'
        self.engine: Engine = self._get_engine()
        self.table = 'interesado_salesforce'
        self.session = self._get_session()

    def _get_engine(self):
        return create_engine(
            url=f'{self.db_type}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}',
        )

    def _get_session(self):
        Session_obj = sessionmaker(bind=self.engine)
        session: Session = Session_obj()
        return session

    def findRecentEmails(
        self,
        email: str,
        current_datetime: datetime,
        past_datetime: datetime,
        more_than_one_record: bool
    ):
        """
        search if interesadoLanding email has done already a "consulta",
        in the last x amount of minutes
        """
        response = self.session.query(InteresadoSalesforce).filter(
            and_(
                InteresadoSalesforce.email.like(f"%{email}%"),
                InteresadoSalesforce.create_date <= current_datetime,
                InteresadoSalesforce.create_date > past_datetime,
            )
        )
        # if you want multiple records
        if more_than_one_record:
            return response
        else:
            return response.first()

    def createInteresadoSalesforce(
        self,
        createLanding: CreateLandingDto
    ):
        create_date = datetime.now().replace(microsecond=0)
        interesado = InteresadoSalesforce(
            nombre=createLanding.nombre,
            apellido=createLanding.apellido,
            email=createLanding.particular,
            telefono=createLanding.telefono,
            ciudad=createLanding.ciudad,
            pais=createLanding.pais,
            nivel_estudio=None,
            id_prod_mkt=createLanding.idprodmkt,
            consulta=createLanding.consulta,
            comercial_id=None,
            utm_source=createLanding.utm_source,
            utm_medium=createLanding.utm_medium,
            utm_campaign=createLanding.utm_campaign,
            utm_content=createLanding.utm_content,
            nombre_referidor=createLanding.nombre_referidor,
            apellido_referidor=createLanding.apellido_referidor,
            particular_referidor=createLanding.particular_referidor,
            url_landing=createLanding.url_landing,
            high_school_status=createLanding.high_school_status,
            utm_term=createLanding.utm_term,
            convalidar=createLanding.convalidar,
            canal=createLanding.canal,
            origen=createLanding.origen,
            suborigen=createLanding.suborigen,
            cohorte_inversion=createLanding.cohorte_inversion,
            create_date=create_date
        )
        try:
            self.session.add(interesado)
            self.session.commit()
            return interesado
        except Exception:
            return {}
