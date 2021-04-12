from app.entities.product import Product
from app.entities import session
from app.exceptions import EntityNotFound, EntityAlreadyExists
from datetime import datetime

class ProductRepository():
  ''' ProductRepository '''

  def __init__(self, session):
    self.session = session
  
  def get_by_id(self, product_id: str) -> Product:
    ''' Return a product or fail '''
    product: Product = self.session.query(Product)\
      .filter_by(id = product_id)\
      .first()
    if not product:
      raise EntityNotFound(f'Product {product_id} was not found')
    return product
  
  def get_by_company(self, company_id: str) -> list:
    ''' Return a list of all company products '''
    products: Product = self.session.query(Product)\
      .filter_by(company_id = company_id)
    return list(products)
  
  def get_all(self) -> list:
    ''' Return a list of all products '''
    products = self.session.query(Product)
    return list(products)

  def add(self, company_id, product_id: str, value: float) -> Product:
    ''' Validate if is an existent product. If not, create. '''
    try:
      if self.get_by_id(product_id):
        raise EntityAlreadyExists(f'Product {product_id} already exists')
    except Exception as e:
      if not isinstance(e, EntityNotFound):
        raise e

    product = Product(product_id, company_id, value)
    self.session.add(product)
    self.session.commit()
    return product
  
  def delete(self, product: Product):
    ''' Delete product '''
    self.session.delete(product)
    self.session.commit()
  