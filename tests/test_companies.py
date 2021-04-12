import pytest
from app.repositories.company_repository import CompanyRepository
from app.entities.company import Company
from app.entities import session
from pytest_mock import mocker
from app.exceptions import EntityNotFound, EntityAlreadyExists
from app.views.companies_view import CompaniesView
import json 
import aiohttp

@pytest.fixture()
def request_mock():
  class RequestMock(object):
    def __init__(self):
      self.headers = {"Authorization": "Basic YWRtaW46c2VjcmV0X2tleQ=="}
  return RequestMock()

@pytest.fixture()
def company():
  return Company('claro_11')

@pytest.fixture()
def companies():
  return [Company('claro_11'), Company('claro_13'), Company('claro_15')]

@pytest.fixture(scope='session')
def company_repository():
  return CompanyRepository(session)

def test_get_company(mocker, company_repository, company):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=company)
  company = company_repository.get_by_id('claro_11')
  assert company
  assert isinstance(company, Company)
  assert company.to_dict()

def test_get_company_fails(mocker, company_repository):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=None)
  with pytest.raises(EntityNotFound):
    company = company_repository.get_by_id('claro_10')

def test_get_all_companies(mocker, company_repository, companies):
  mocker.patch('sqlalchemy.orm.query.Query.filter_by', return_value=companies)
  companies = company_repository.get_all()
  assert isinstance(companies, list)

def test_create_company(mocker, company_repository, company):
  mocker.patch('app.entities.session.add', return_value=None)
  mocker.patch('app.entities.session.commit', return_value=None)
  mocker.patch('app.repositories.company_repository.CompanyRepository.get_by_id', return_value=None)
  company = company_repository.add(company.id)
  assert company.id is not None
  assert company.to_dict()
  assert isinstance(company, Company)

def test_create_company_fail(mocker, company_repository, company):
  mocker.patch('app.entities.session.add', return_value=None)
  mocker.patch('app.entities.session.commit', return_value=None)
  mocker.patch('app.repositories.company_repository.CompanyRepository.get_by_id', return_value=company)
  with pytest.raises(EntityAlreadyExists):
    company = company_repository.add(company.id)

def test_delete_company(mocker, company_repository, company):
  mocker.patch('app.entities.session.delete', return_value=None)
  mocker.patch('app.entities.session.commit', return_value=None)
  company_repository.delete(company)
  assert company.id is not None

@pytest.mark.asyncio
async def test_company_index(mocker, companies):
  mocker.patch('sqlalchemy.orm.query.Query.filter_by', return_value=companies)
  response = await CompaniesView.index({})
  assert response.status == 200
  json.loads(response.text)