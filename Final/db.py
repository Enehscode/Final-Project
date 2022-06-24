from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# El engine permite a SQLAlchemy comunicarse con la base de datos
# https://docs.sqlalchemy.org/en/14/core/engines.html

# Conectarse a un base de datos SQLite
engine = create_engine("sqlite:///database/drugstore.db")

#Nos permite realizar operaciones dentro de la bd
Session = sessionmaker(bind=engine)
session = Session()

#Buscará todas las clases que estructuran una tabla de bd
# y la mapeará y creará las tablas en la bd
Base = declarative_base()