from app.schemas.env_schemas import MysqlAdenFormsSchema
from sqlalchemy import (
    create_engine,
    Engine,
    #    Connection,
    # inspect,
    #    select,
    #    insert,
    # Column,
    # String,
    # Integer,
    #    CHAR,
    # Date,
    # Boolean,
    # or_,
    and_,
)
# from pydantic import BaseModel, Field
# from sqlalchemy.sql import text
from sqlalchemy.orm import (
    sessionmaker,
    Session,
    # declarative_base
)
from abc import ABC, abstractmethod
from datetime import datetime
from app.modules.landings.interesado_salesforce_entity import InteresadoSalesforce
# Base = declarative_base()


# class InteresadoSalesforce(Base):
#     __tablename__ = 'interesado_salesforce'

#     id = Column('id', Integer, primary_key=True, autoincrement=True)
#     nombre = Column('nombre', String(255))
#     apellido = Column('apellido', String(255))
#     email = Column('email', String(255))
#     telefono = Column('telefono', String(255))
#     ciudad = Column('ciudad', String(255))
#     pais = Column('pais', String(255))
#     nivel_estudio = Column('nivel_estudio', String(255), nullable=True, default=None)
#     id_prod_mkt = Column('id_prod_mkt', String(255))
#     consulta = Column('consulta', String)
#     comercial_id = Column('comercial_id', String(255), nullable=True, default=None)
#     utm_source = Column('utm_source', String(255))
#     utm_medium = Column('utm_medium', String(255))
#     utm_campaign = Column('utm_campaign', String(255))
#     utm_content = Column('utm_content', String(255), nullable=True, default=None)
#     error = Column('error', String(255))
#     create_date = Column('create_date', Date, nullable=True, default=None)
#     nombre_referidor = Column('nombre_referidor', String(255))
#     apellido_referidor = Column('apellido_referidor', String(255), nullable=True, default=None)

#     particular_referidor = Column(
#         'particular_referidor', String(255), nullable=True, default=None
#     )
#     url_landing = Column('url_landing', String(255), nullable=True, default=None)
#     facebook_lead_id = Column('facebook_lead_id', String(255), nullable=True, default=None)
#     facebook_event_id = Column('facebook_event_id', String(255), nullable=True, default=None)
#     facebook_client_ip_address = Column(
#         'facebook_client_ip_address', String(100), nullable=True, default=None
#     )
#     facebook_client_user_agent = Column(
#         'facebook_client_user_agent', String(100), nullable=True, default=None
#     )
#     high_school_status = Column('high_school_status', String(100), nullable=True, default=None)
#     utm_term = Column('utm_term', String(255), nullable=True, default=None)
#     convalidar = Column('convalidar', Boolean, nullable=True, default=None)
#     canal = Column('canal', String(100), nullable=True, default=None)
#     origen = Column('origen', String(100), nullable=True, default=None)
#     suborigen = Column('suborigen', String(100), nullable=True, default=None)
#     cohorte_inversion = Column('cohorte_inversion', String(100), nullable=True, default=None)


# class MysqlAdenFormsSchema(BaseModel):
#     mysql_host: str
#     mysql_port: int
#     mysql_user: str
#     mysql_password: str = Field(default='')
#     mysql_db: str


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
        if more_than_one_record:
            return response
        else:
            return response.first()

    def saveInteresadoSalesforce(
        self,
        nombre,
        apellido,
        email,
        telefono,
        ciudad,
        pais,
        nivel_estudio,
        id_prod_mkt,
        consulta,
        comercial_id,
        utm_source,
        utm_medium,
        utm_campaign,
        utm_content,
        error,
        create_date,
        nombre_referidor,
        apellido_referidor,
        particular_referidor,
        url_landing,
        facebook_lead_id,
        facebook_event_id,
        facebook_client_ip_address,
        facebook_client_user_agent,
        high_school_status,
        utm_term,
        convalidar,
        canal,
        origen,
        suborigen,
        cohorte_inversion,
    ):
        interesado = InteresadoSalesforce(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            ciudad=ciudad,
            pais=pais,
            nivel_estudio=nivel_estudio,
            id_prod_mkt=id_prod_mkt,
            consulta=consulta,
            comercial_id=comercial_id,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_content=utm_content,
            error=error,
            create_date=create_date,
            nombre_referidor=nombre_referidor,
            apellido_referidor=apellido_referidor,
            particular_referidor=particular_referidor,
            url_landing=url_landing,
            facebook_lead_id=facebook_lead_id,
            facebook_event_id=facebook_event_id,
            facebook_client_ip_address=facebook_client_ip_address,
            facebook_client_user_agent=facebook_client_user_agent,
            high_school_status=high_school_status,
            utm_term=utm_term,
            convalidar=convalidar,
            canal=canal,
            origen=origen,
            suborigen=suborigen,
            cohorte_inversion=cohorte_inversion,
        )
        self.session.add(interesado)
        self.session.commit()


# if __name__ == '__main__':
#     aden_form_settings = MysqlAdenFormsSchema(
#         mysql_user='datosweb',
#         mysql_password='h0m3r0',
#         mysql_db='ADEN_forms',
#         mysql_host='10.158.0.37',
#         mysql_port=3306

#     )
#     aden_forms = AdenForms(aden_form_settings)
#     # aden_forms.engine: Engine = aden_forms.get_connection()
#     # Base.metadata.create_all(bind=engine)
#     insp = inspect(aden_forms.engine)
#     print(insp.get_table_names())
#     Session_obj = sessionmaker(bind=aden_forms.engine)
#     session: Session = Session_obj()

#     # result = session.get(InteresadoSalesforce, {'id': 39671})
#     # print(result.nombre)

#     # results = session.query(InteresadoSalesforce).filter(
#     #     InteresadoSalesforce.nombre.like('%Zurisada%'))
#     # for r in results:
#     #     print(r)

#     int_sf = InteresadoSalesforce(
#         nombre='test',
#         apellido='test',
#         telefono='test',
#         email='test',
#         ciudad='test',
#         pais='test',
#         id_prod_mkt='test',
#         consulta='test',
#         utm_source='test',
#         utm_medium='test',
#         utm_campaign='test',
#         error='test',
#         nombre_referidor='test'
#     )
#     # session.add(int_sf)
#     # session.commit()

#     result = aden_forms.findRecentEmails(email='baezreynosojunior@gmail.com')
#     for r in result:
#         print(r.id)
#     # print(dir(results))
#     # result = session.get(InteresadoSalesforce, {'nombre': 'Zurisaday'})
#     session.close()
#     # print(session.get(entity=aden_forms.table))
#     # conn: Connection = engine.connect()
