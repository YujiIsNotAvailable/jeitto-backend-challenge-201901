from app.security import md5_hash, is_authenticated
from app.entities.user import User
from aiohttp import web_request
import pytest
from pytest_mock import mocker
from datetime import datetime, timedelta
from app.exceptions import EntityNotFound, DomainException

@pytest.fixture()
def user():
  user = User('username', 'password')
  user.id = 1
  return user

@pytest.mark.parametrize('string, hashed', [
  ('senha123', 'e7d80ffeefa212b7c5c55700e4f7193e'),
  ('123456', 'e10adc3949ba59abbe56e057f20f883e'),
  ('s@meStr1ng', '4ae447c1c4953c489f1717801a4f0ed3')
])
def test_md5_hash(string, hashed):
  assert md5_hash(string) == hashed

@pytest.mark.asyncio
async def test_is_authenticated(mocker, user):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=user)
  mocker.patch('app.security.__jwt_authorization_decode_by_request', return_value={'id': 1,'expiration_date': (datetime.now() + timedelta(hours=24)).isoformat()})
  @is_authenticated
  def mock_func(*args):
    pass
  await mock_func([])

@pytest.mark.asyncio
async def test_is_authenticated_fail_expiration_date(mocker, user):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=user)
  mocker.patch('app.security.__jwt_authorization_decode_by_request', return_value={'id': 1,'expiration_date': datetime.now().isoformat()})
  @is_authenticated
  async def mock_func(*args):
    pass
  response = await mock_func([])
  assert response.status == 401

@pytest.mark.asyncio
async def test_is_authenticated_fail_user(mocker):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=None)
  mocker.patch('app.security.__jwt_authorization_decode_by_request', return_value={'id': 1,'expiration_date': (datetime.now() + timedelta(hours=24)).isoformat()})
  @is_authenticated
  async def mock_func(*args):
    pass
  response = await mock_func([])
  assert response.status == 401