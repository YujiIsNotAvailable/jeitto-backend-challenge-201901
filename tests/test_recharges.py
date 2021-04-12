import pytest
from pytest_mock import mocker
from app.repositories.recharge_repository import RechargeRepository
from app.entities.product import Product
from app.entities.recharge import Recharge
from app.entities import session
from app.exceptions import EntityNotFound

@pytest.fixture()
def product():
  return Product('claro_11', 'claro_10', 10)

@pytest.fixture()
def recharge(product):
  return Recharge(product, 11999999999)

@pytest.fixture()
def recharges(product):
  return [Recharge(product, 11999999999), Recharge(product, 11999999999), Recharge(product, 11999999999)]

@pytest.fixture()
def recharge_repository():
  return RechargeRepository(session)

def test_get_all_recharges(mocker, recharge_repository, recharges):
  mocker.patch('sqlalchemy.orm.query.Query.filter_by', return_value=recharges)
  recharges: list = recharge_repository.get_all()
  assert isinstance(recharges, list)
  for recharge in recharges:
    assert isinstance(recharge, Recharge)

def test_get_recharges_by_phone_number(mocker, recharge_repository, recharges):
  mocker.patch('sqlalchemy.orm.query.Query.filter_by', return_value=recharges)
  phone_number = 11999999999
  recharges = recharge_repository.get_by_phone_number(phone_number)
  assert isinstance(recharges, list)
  for recharge in recharges:
    assert isinstance(recharge, Recharge)
    assert recharge.phone_number == phone_number

def test_get_recharge_by_id(mocker, recharge_repository, recharge):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=recharge)
  recharge = recharge_repository.get_by_id(recharge.id)
  assert isinstance(recharge, Recharge)

def test_get_recharge_by_id_fail(mocker, recharge_repository, recharge):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=None)
  with pytest.raises(EntityNotFound):
    recharge = recharge_repository.get_by_id(recharge.id)

def test_do_recharge(mocker, recharge_repository, product):
  mocker.patch('app.repositories.product_repository.ProductRepository.get_by_id', return_value=product)
  mocker.patch('app.entities.session.commit', return_value=None)
  phone_number = 11999999999
  recharge = recharge_repository.do_recharge(product.company_id, product.id, phone_number)
  assert isinstance(recharge, Recharge)
  assert recharge.phone_number == phone_number
