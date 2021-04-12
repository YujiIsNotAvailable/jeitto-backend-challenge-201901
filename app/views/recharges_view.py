from aiohttp import web
from app.repositories.recharge_repository import RechargeRepository
from app.exceptions import DomainException
from app.entities import session
import json

class RechargesView(web.View):
  ''' RechargesView
    Handles recharge requests according to the situation 
  '''
  async def index(request):
    '''
      Search a list of recharges. 
      If requested with phone_number: returns all products from phone_number, 
      else, returns all recharges in db
    '''
    try:
      repository = RechargeRepository(session)

      phone_number: str = request.url.query['phone_number'] if request.url.query else None
      
      if phone_number:
        recharges = repository.get_by_phone_number(phone_number)
      else:
        recharges = repository.get_all()

      return web.Response(text=json.dumps([recharge.to_dict() for recharge in recharges]), status=200)
    except Exception as e:
      print(e)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)
  
  async def show(request):
    ''' Get a recharge from id '''
    try:
      recharge_id = request.match_info['id']
      repository = RechargeRepository(session)

      product = repository.get_by_id(recharge_id)
      return web.Response(text=json.dumps(product.to_dict()), status=200)
    except Exception as e:
      print(e)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)
  
  async def recharge(request):
    ''' Recharge a phone and returns a recharge '''
    try:
      payload: object = json.loads(await request.text())
      repository = RechargeRepository(session)

      recharge = repository.do_recharge(payload['company_id'], payload['product_id'], payload['phone_number'])
      return web.Response(text=json.dumps(recharge.to_dict()), status=201)
    except Exception as e:
      print(e)
      if isinstance(e, DomainException):
        web.Response(text=f'Não foi possível efetuar a recarga para {phone_number}.', status=422)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)
