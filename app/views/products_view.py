from aiohttp import web
from app.repositories.product_repository import ProductRepository
from app.repositories.company_repository import CompanyRepository
from app.exceptions import EntityAlreadyExists
from app.security import is_authenticated
from app.entities import session
import json

class ProductsView(web.View):
  ''' ProductsView
    Handles product requests according to the situation 
  '''
  async def index(request):
    '''
      Search a list of products. 
      If requested with company_id: returns all products of this company, 
      else, returns all products in db
    '''
    try:
      repository = ProductRepository(session)
      try:
        company_id = request.url.query['company_id']
      except KeyError:
        company_id = None

      if company_id:
        products = repository.get_by_company(company_id)
        companies_products = {
          "company": company_id,
          "products": [ product.to_dict() for product in products ]
        }
      else:
        companies_products = []
        company_repository = CompanyRepository(session)
        companies = company_repository.get_all()
        for company in companies:
          companies_products.append({
            "company": company.id,
            "products": [ product.to_dict() for product in company.products ]
          })

      return web.Response(text=json.dumps(companies_products), status=200)
    except Exception as e:
      print(e)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)
  
  async def show(request):
    ''' Returns a product from id '''
    try:
      product_id = request.match_info['id']
      repository = ProductRepository(session)

      product = repository.get_by_id(product_id)
      return web.Response(text=json.dumps(product.to_dict()), status=200)
    except Exception as e:
      print(e)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)

    
  @is_authenticated
  async def store(request):
    ''' Stores a new product '''
    try:
      payload = json.loads(await request.text())
      company_id = payload['company_id']
      product_id = payload['product_id']
      value = payload['value']
      repository = ProductRepository(session)

      product = repository.add(company_id, product_id, value)
      return web.Response(text=json.dumps(product.to_dict()), status=201)
    except Exception as e:
      print(e)
      if isinstance(e, EntityAlreadyExists):
        return web.Response(text=f'Produto {product_id} já existe.', status=422)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)

  @is_authenticated
  async def destroy(request):
    ''' Deletes a product '''
    try:
      product_id = request.match_info['id']
      repository = ProductRepository(session)
      product = repository.get_by_id(product_id)
      repository.delete(product)
      return web.Response(status=204)
    except:
      print(e)
      if isinstance(e, EntityNotFound):
        return web.Response(text=f'Produto {product_id} não foi encontrada.', status=404)
      return web.Response(text="Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.", status=500)
