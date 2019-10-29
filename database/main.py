import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from database.database_info import DB_PATH

from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
