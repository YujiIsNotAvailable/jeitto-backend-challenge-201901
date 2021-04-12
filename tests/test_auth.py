import pytest
import pytest_mock
from app.entities.user import User 
from app.repositories.user_repository import UserRepository
from app.entities.data.auth import Auth
from app.entities import session
from app.exceptions import DomainException, EntityNotFound
from app.security import md5_hash
from app.views.auth_view import AuthView
from aiohttp.web_request import Request
import json

@pytest.fixture()
def user():
  return User('admin', md5_hash('secret_key').encode())

@pytest.fixture()
def request_mock():
  class RequestMock(object):
    def __init__(self):
      self.headers = {"Authorization": "Basic YWRtaW46c2VjcmV0X2tleQ=="}
  return RequestMock()

@pytest.fixture()
def user_repository():
  return UserRepository(session)

def test_get_user_by_username(mocker, user_repository, user):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=user)
  user = user_repository.get_by_username(user.username)
  assert user.username
  assert isinstance(user, User)

def test_get_user_by_username_fail(mocker, user_repository, user):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=None)
  with pytest.raises(EntityNotFound):
    user = user_repository.get_by_username(user.username)

def test_authentication(mocker, user_repository, user):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=user)
  auth: Auth = user_repository.authenticate(user.username, 'secret_key')
  assert auth.token
  assert auth.expiration_time
  assert isinstance(auth, Auth)

def test_authentication_fail(mocker, user_repository, user):
  mocker.patch('sqlalchemy.orm.query.Query.first', return_value=None)
  user_repository = UserRepository(session)
  with pytest.raises(DomainException):
    auth: Auth = user_repository.authenticate(user.username, user.password)

@pytest.mark.asyncio
async def test_authentication_authenticate(mocker, request_mock, user):
  mocker.patch('app.repositories.user_repository.UserRepository.get_by_username', return_value=user)
  response = await AuthView.authenticate(request_mock)
  data = json.loads(response.text)
  assert response.status == 200
  assert data['token']
  assert data['expiration_time']