from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.entities import EntityBase

class Product(EntityBase):
  ''' Product entity \n
    id -> str : id of product \n
    company_id -> str : id of product \n
    value -> float : Value of product
    created_at -> datetime : datetime the product was created \n
    company: Company relationship ([product] belongs to [company]) \n
    recharges: Recharge relationship ([product] has many [recharges]) \n
  '''
  __tablename__ = 'products'
  id = Column(String(255), primary_key=True)
  company_id = Column(String(255), ForeignKey('companies.id'))
  value = Column(Float, nullable=False)
  created_at = Column(DateTime(), nullable=False, default=datetime.utcnow())
  company = relationship("Company", back_populates="products")
  recharges = relationship("Recharge", back_populates='product')

  def __init__(self, id: str, company_id: str, value: float):
    self.id = id
    self.company_id = company_id
    self.value = value

  def to_dict(self) -> dict :
    ''' Returns a dict of product entity  '''
    return {
      'id': self.id,
      'company_id': self.company_id,
      'value': self.value,
      'created_at': str(self.created_at)
    }