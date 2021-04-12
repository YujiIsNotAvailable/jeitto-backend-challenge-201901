from app.entities.recharge import Recharge
from app.entities.product import Product
from app.entities import session
from app.repositories.product_repository import ProductRepository
from app.exceptions import EntityNotFound, DomainException
from datetime import datetime

class RechargeRepository():
  ''' RechargeRepository '''

  def __init__(self, session):
    self.session = session
  
  def get_by_id(self, recharge_id: str) -> Recharge:
    ''' Return a Recharge or raise exception '''
    recharge: Recharge = self.session.query(Recharge)\
      .filter_by(id = recharge_id)\
      .first()
    if not recharge:
      raise EntityNotFound(f'Recharge {recharge_id} was not found')
    return recharge
  
  def get_all(self) -> list:
    ''' Return a list of all recharges '''
    recharges = self.session.query(Recharge)
    return list(recharges)
  
  def get_by_phone_number(self, phone_number: int) -> list:
    ''' Return a list of all recharges from phone number '''
    recharges = self.session.query(Recharge)\
      .filter_by(phone_number = phone_number)
    print(list(recharges))
    return list(recharges)
  
  def do_recharge(self, company_id: str, product_id: str, phone_number: int) -> Recharge:
    ''' Return Recharge
      Validate if product Company is the same of product_id, then do a recharge with phone_number
    '''
    product_repository = ProductRepository(session)
    product = product_repository.get_by_id(product_id)
    if product.company_id != company_id:
      raise DomainException(f'Product {product_id} dont belongs to company {company_id}')
    recharge = Recharge(product.id, phone_number)
    self.session.add(recharge)
    self.session.commit()
    return recharge
  