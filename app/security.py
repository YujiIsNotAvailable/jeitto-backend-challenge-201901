from app.repositories.user_repository import UserRepository
from aiohttp import web
from datetime import datetime
from app.entities import session, SECRET_KEY
from app.exceptions import EntityNotFound
import hashlib
import jwt

def is_authenticated(func):
  ''' Authentication decorator \n
    Checks if user is authenticated from request token.
  '''
  async def wrapper(*args):
    try:
      request = args[0]
      payload = __jwt_authorization_decode_by_request(request, SECRET_KEY, "HS256")

      if payload == False: 
        return web.Response(text="Necessário token de autenticação.", status=403)

      user_id = payload['id']
      expiration_date = datetime.fromisoformat(payload['expiration_date'])
      repository = UserRepository(session)
      user = repository.get_by_id(user_id)
      if (expiration_date < datetime.now()):
        return web.Response(text='Token está expirado. Realize novamente a autenticação.', status=401)

      return await func(request) if func else None
    except Exception as e:
      print(e)
      if isinstance(e, EntityNotFound):
        return web.Response(text="Usuário/senha incorreto(s)", status=401)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)
  return wrapper

def md5_hash(passphrase: str) -> str :
  md5 = hashlib.md5()
  md5.update(passphrase.encode('utf-8'))
  return md5.hexdigest()
  
def __jwt_authorization_decode_by_request(request, secret: str, algorithms: str):
  ''' Returns authorization '''
  try:
    header = request.headers['Authorization']
    return jwt.decode(header[len("Bearer "):], secret, algorithms=algorithms)
  except KeyError as e:
    print(e)
    return False