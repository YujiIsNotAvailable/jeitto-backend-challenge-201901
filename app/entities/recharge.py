from sqlalchemy import Column, String, ForeignKey, BigInteger, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.entities.product import Product
from app.entities import EntityBase

class Recharge(EntityBase):
  ''' Recharge entity \n
    id -> str : id of recharge \n
    product_id -> str : id of product \n
    phone_number -> int : recharge's phone number \n
    created_at -> datetime : datetime the recharge was made \n
    product: Product relationship ([recharge] belongs to [product]) \n
  '''
  __tablename__ = 'recharges'
  id = Column(Integer, primary_key=True)
  product_id = Column(String(255), ForeignKey('products.id'))
  phone_number = Column(BigInteger, nullable=False)
  created_at = Column(DateTime(), nullable=False, default=datetime.utcnow())
  product = relationship("Product", back_populates="recharges")

  def __init__(self, product_id: str, phone_number: int):
    self.product_id = product_id
    self.phone_number = phone_number

  def to_dict(self) -> dict :
    ''' Returns a dict of recharge entity  '''
    return {
      'id': self.id,
      'product_id': self.product_id,
      'phone_number': self.phone_number,
      'created_at': str(self.created_at)
    }