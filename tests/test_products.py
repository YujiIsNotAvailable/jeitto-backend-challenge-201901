import pytest
from pytest_mock import mocker
from app.entities import session
from app.entities.product import Product
from app.entities.company import Company
from app.repositories.product_repository import ProductRepository
from app.exceptions import EntityNotFound, EntityAlreadyExists

@pytest.fixture()
def product():
  return Product('claro_11', 'claro_10', 10)

@pytest.fixture()
def company_products():
  return [Product('claro_11', 'claro_10', 10), Product('claro_11', 'claro_20', 20), Product('claro_11', 'claro_30', 30)]

@pytest.fixture()
def company():
  return Company('claro_11')

@pytest.fixture()
def product_repository(scope='session'):
  return ProductRepository(session)

def test_get_product_by_id(mocker, product_repository, product):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=product)
  product: Product = product_repository.get_by_id(product.id)
  assert product.id
  assert product.value
  assert isinstance(product, Product)

def test_get_product_by_id_fail(mocker, product_repository, product):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=None)
  with pytest.raises(EntityNotFound):
    product_repository.get_by_id(product.id)

def test_get_products_by_company(mocker, product_repository, company_products, company):
  mocker.patch('sqlalchemy.orm.query.Query.filter_by', return_value=company_products)
  products: list = product_repository.get_by_company(company.id)
  assert isinstance(products, list)
  for product in products:
    assert isinstance(product, Product)

def test_get_all_products(mocker, product_repository, company_products):
  mocker.patch('sqlalchemy.orm.query.Query.filter_by', return_value=company_products)
  products: list = product_repository.get_all()
  assert isinstance(products, list)
  for product in products:
    assert isinstance(product, Product)

def test_create_product(mocker, product_repository, product, company):
  mocker.patch('app.entities.session.add', return_value=None)
  mocker.patch('app.entities.session.commit', return_value=None)
  mocker.patch('app.repositories.product_repository.ProductRepository.get_by_id', return_value=None)
  product = product_repository.add(company.id, product.id, product.value)
  assert product.id is not None
  assert product.to_dict()
  assert isinstance(product, Product)

def test_create_product_fail(mocker, product_repository, product, company):
  mocker.patch('app.entities.session.add', return_value=None)
  mocker.patch('app.entities.session.commit', return_value=None)
  mocker.patch('app.repositories.product_repository.ProductRepository.get_by_id', return_value=product)
  with pytest.raises(EntityAlreadyExists):
    product = product_repository.add(company.id, product.id, product.value)

def test_delete_product(mocker, product_repository, product):
  mocker.patch('app.entities.session.delete', return_value=None)
  mocker.patch('app.entities.session.commit', return_value=None)
  product_repository.delete(product)
  assert product.id is not None