from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.entities import EntityBase

class User(EntityBase):
  ''' User entity \n
    id -> str : id of recharge \n
    username -> str : username \n
    password -> str : varbinary md5 password \n
    created_at -> datetime : datetime the user was created \n
  '''
  __tablename__ = 'users'
  id = Column(String(255), primary_key=True)
  username = Column(String(255), nullable=False)
  password = Column(String(255), nullable=False)
  created_at = Column(DateTime(), nullable=False, default=datetime.utcnow())

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

  def to_dict(self) -> dict:
    ''' Returns a dict of user entity  '''
    return {
      id: self.id,
      username: self.username,
      password: self.password,
      created_at: str(self.created_at)
    }