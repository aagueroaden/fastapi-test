from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Boolean,
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class InteresadoSalesforce(Base):
    __tablename__ = 'interesado_salesforce'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nombre = Column('nombre', String(255))
    apellido = Column('apellido', String(255))
    email = Column('email', String(255))
    telefono = Column('telefono', String(255))
    ciudad = Column('ciudad', String(255))
    pais = Column('pais', String(255))
    nivel_estudio = Column('nivel_estudio', String(255), nullable=True, default=None)
    id_prod_mkt = Column('id_prod_mkt', String(255))
    consulta = Column('consulta', String)
    comercial_id = Column('comercial_id', String(255), nullable=True, default=None)
    utm_source = Column('utm_source', String(255))
    utm_medium = Column('utm_medium', String(255))
    utm_campaign = Column('utm_campaign', String(255))
    utm_content = Column('utm_content', String(255), nullable=True, default=None)
    error = Column('error', String(255))
    create_date = Column('create_date', Date, nullable=True, default=None)
    nombre_referidor = Column('nombre_referidor', String(255))
    apellido_referidor = Column('apellido_referidor', String(255), nullable=True, default=None)

    particular_referidor = Column('particular_referidor', String(255), nullable=True, default=None)
    url_landing = Column('url_landing', String(255), nullable=True, default=None)
    facebook_lead_id = Column('facebook_lead_id', String(255), nullable=True, default=None)
    facebook_event_id = Column('facebook_event_id', String(255), nullable=True, default=None)
    facebook_client_ip_address = Column(
        'facebook_client_ip_address', String(100), nullable=True, default=None
    )
    facebook_client_user_agent = Column(
        'facebook_client_user_agent', String(100), nullable=True, default=None
    )
    high_school_status = Column('high_school_status', String(100), nullable=True, default=None)
    utm_term = Column('utm_term', String(255), nullable=True, default=None)
    convalidar = Column('convalidar', Boolean, nullable=True, default=None)
    canal = Column('canal', String(100), nullable=True, default=None)
    origen = Column('origen', String(100), nullable=True, default=None)
    suborigen = Column('suborigen', String(100), nullable=True, default=None)
    cohorte_inversion = Column('cohorte_inversion', String(100), nullable=True, default=None)
