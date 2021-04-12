from aiohttp import web
from app.repositories.company_repository import CompanyRepository
from app.entities import session
from app.entities.company import Company
from app.exceptions import EntityNotFound, EntityAlreadyExists
from app.security import is_authenticated
import json

class CompaniesView(web.View):
  ''' CompaniesView
    Handles companies requests according to the situation 
  '''
  async def index(request):
    ''' Get a list of all companies '''
    try:
      repository = CompanyRepository(session)
      companies = repository.get_all()
      return web.Response(text=json.dumps([company.to_dict() for company in companies]), status=200)
    except Exception as e:
      print (e)
      return web.Response(text='Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.', status=500)
  
  async def show(request):
    ''' Get company by id '''
    try:
      repository = CompanyRepository(session)
      data = request.match_info
      company_id: str = data['id']
      company: Company = repository.get_by_id(company_id)
      
      if not company:
        return web.Response(text="Companhia {company_id} não foi encontrada :(", status=404)
      return web.Response(text=json.dumps(company.to_dict()), status=200)
    except Exception as e:
      print (e)
      if isinstance(e, EntityNotFound):
        return web.Response(text=f'Companhia {company_id} não foi encontrada.', status=404)
      return web.Response(text='Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.', status=500)
  
  @is_authenticated
  async def store(request):
    ''' Stores a new company '''
    try:
      payload = json.loads(await request.text())
      repository = CompanyRepository(session)
      company_id: str = payload['id']
      company: Company = repository.add(company_id)
      return web.Response(text=json.dumps(company.to_dict()), status=201)
    except Exception as e:
      print (e)
      if isinstance(e, EntityAlreadyExists):
        return web.Response(text=f'Companhia {company_id} já existe.', status=409)
      return web.Response(text='Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.', status=500)
  
  @is_authenticated
  async def destroy(request):
    ''' Destroy a company '''
    try:
      payload = request.match_info
      repository = CompanyRepository(session)
      company_id: str = payload['id']
      company: Company = repository.get_by_id(company_id)
      repository.delete(company)
      return web.Response(status=204)
    except Exception as e:
      print(e)
      if isinstance(e, EntityNotFound):
        return web.Response(text=f'Companhia {company_id} não foi encontrada.', status=404)
      return web.Response(text='Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.', status=500)
