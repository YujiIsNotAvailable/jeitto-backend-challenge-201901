import sqlalchemy
from sqlalchemy_utils import database_exists
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
from sqlalchemy.orm import sessionmaker

MYSQL_HOST = config('MYSQL_HOST')
MYSQL_PORT = config('MYSQL_PORT')
MYSQL_USER = config('MYSQL_USER')
MYSQL_PASSWORD = config('MYSQL_PASSWORD')
MYSQL_DATABASE = config('MYSQL_DATABASE')
SECRET_KEY = config('SECRET_KEY')

url = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
if not database_exists(url):
  raise Exception("Database "+MYSQL_DATABASE + " was not found on "+MYSQL_HOST+MYSQL_PORT)

engine = sqlalchemy.create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()

EntityBase = declarative_base()