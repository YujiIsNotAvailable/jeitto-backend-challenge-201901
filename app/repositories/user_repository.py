from app.exceptions import DomainException, EntityNotFound
from app.entities.user import User
from app.entities.data.auth import Auth
from app.entities import SECRET_KEY
from datetime import datetime, timedelta
import app
import jwt

class UserRepository():
  ''' UserRepository '''

  def __init__(self, session):
    self.session = session

  def get_by_id(self, id: int) -> User :
    user: User = self.session.query(User)\
      .filter_by(id=id)\
      .first()
    if not user:
      raise EntityNotFound(f'User {id} was not found')
    return user

  def get_by_username(self, username: str) -> User :
    user: User = self.session.query(User)\
      .filter_by(username=username)\
      .first()
    if not user:
      raise EntityNotFound(f'User {username} was not found')
    return user

  def authenticate(self, username: str, password: str) -> Auth :
    ''' Validate user and password and returns a Auth instance 
      May raise an exception if user / password does not match
    '''
    try:
      user: User = self.get_by_username(username)
      md5_password = app.security.md5_hash(password)
      if user.password.decode() != md5_password:
        raise DomainException

      expiration_date = (datetime.now() + timedelta(hours=24)).isoformat()
      token: str = jwt.encode({
        "id": user.id,
        "expiration_date": expiration_date
      }, SECRET_KEY)

      return Auth(token, expiration_date)
    except Exception as e:
      print(e)
      if isinstance(e, (DomainException, EntityNotFound)):
        raise DomainException('Wrong user/password')
      raise e
