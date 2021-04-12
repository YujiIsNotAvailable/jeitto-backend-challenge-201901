from app.entities.company import Company
from app.exceptions import EntityNotFound, EntityAlreadyExists
from datetime import datetime
from app.repositories.product_repository import ProductRepository

class CompanyRepository():
  ''' CompanyRepository '''

  def __init__(self, session):
    self.session = session
    
  def get_by_id(self, company_id: str) -> Company:
    ''' Return a Company or fail '''
    company: Company = self.session.query(Company)\
      .filter_by(id = company_id)\
      .first()
    if not company:
      raise EntityNotFound(f'Company {company_id} was not found')
    return company
    
  def get_all(self) -> list :
    ''' Return a list of all companies (not deleted) '''
    companies = self.session.query(Company)
    return list(companies)
  
  def add(self, company_id: str) -> Company:
    ''' Validate if is an existent company. If not, create. '''
    try:
      if self.get_by_id(company_id):
        raise EntityAlreadyExists(f'Company {company_id} already exists')
    except Exception as e:
      if not isinstance(e, EntityNotFound):
        raise e
    company = Company(company_id)
    self.session.add(company)
    self.session.commit()
    return company
  
  def delete(self, company: Company):
    ''' Delete company and all his products '''
    if company.products:
      product_repository = ProductRepository(self.session)
      for product in company.products:
        product_repository.delete(product)
    self.session.delete(company)
    self.session.commit()
