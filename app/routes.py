from app.views.companies_view import CompaniesView
from app.views.products_view import ProductsView
from app.views.recharges_view import RechargesView
from app.views.auth_view import AuthView
from aiohttp import web

def get() ->list :
  ''' Returns a list of web routes configurated '''
  return [
    web.get('/companies', CompaniesView.index),
    web.get('/companies/{id}', CompaniesView.show),
    web.post('/companies', CompaniesView.store),
    web.delete('/companies/{id}', CompaniesView.destroy),

    web.get('/products', ProductsView.index),
    web.get(r'/products/{id:\d+}', ProductsView.show),
    web.post('/products', ProductsView.store),
    web.delete('/products/{id}', ProductsView.destroy),

    web.get('/recharges', RechargesView.index),
    web.get('/recharges/{id}', RechargesView.show),
    web.post('/recharges', RechargesView.recharge),
    
    web.post('/auth', AuthView.authenticate)
  ]
