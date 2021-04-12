from aiohttp import web
from app import webapp
import sys

if __name__ == '__main__':
  try:
    with open(".env"):
      pass
  except IOError:
    print('Missing .env file.')
    sys.exit()

  web.run_app(webapp, port=5000)