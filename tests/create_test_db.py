import sqlite3
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.orm import sessionmaker

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "test.db")

engine = sqlalchemy.create_engine(f'sqlite:////{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

create_db_script = open('./create_test_db.sql', 'r').read()
cursor.executescript(create_db_script)
connection.commit()
