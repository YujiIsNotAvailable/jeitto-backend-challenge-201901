from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from app.entities import EntityBase
from app.entities.product import Product
from datetime import datetime

class Company(EntityBase):
  ''' Company entity \n
    id -> str : id of company \n
    created_at -> datetime : datetime the company was created \n
    products: Product relationship ([company] to many [products]) \n
  '''
  __tablename__ = 'companies'
  id = Column(String(255), primary_key=True)
  created_at = Column(DateTime(), nullable=False, default=datetime.utcnow())
  products = relationship("Product", back_populates="company")

  def __init__(self, id: str):
    self.id = id

  def to_dict(self) -> dict :
    ''' Returns a dict of company entity  '''
    return {
      'id': self.id,
      'created_at': str(self.created_at)
    }
