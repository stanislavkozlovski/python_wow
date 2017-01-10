import sqlite3

from database.database_info import DB_PATH
# TODO: Add SQLAlchemy

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
