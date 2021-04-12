from aiohttp import web
from app.repositories.user_repository import UserRepository
from app.entities.data.auth import Auth
from app.exceptions import DomainException
from app.entities import session
import base64
import json

class AuthView(web.View):
  ''' AuthView 
    Handles auth requests 
  '''

  async def authenticate(request):
    ''' Returns a json with token and expiration_date (needed for anothers requests)
      Unpacks user and password from authorization for validation.
    '''
    try:
      try:
        authorization = request.headers['Authorization']
      except:
        return web.Response(text="Dados para autenticação necessários.", status=403)
      encoded = authorization[len("Basic "):]
      binary = base64.b64decode(encoded)
      packed = binary.decode().split(":", 2)

      username: str = packed[0]
      password: str = packed[1]

      user_repository = UserRepository(session)
      auth: Auth = user_repository.authenticate(username, password)
      return web.Response(text=json.dumps({'token': auth.token, 'expiration_time': auth.expiration_time}), status=200)
    except Exception as e:
      print(e)
      if isinstance(e, DomainException):
        return web.Response(text='Usuário e/ou senha incorreta. Por favor, tente novamente.', status=403)  
      return web.Response(text='Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.', status=500)