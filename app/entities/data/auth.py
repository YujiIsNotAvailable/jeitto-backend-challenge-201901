class Auth():
  ''' Auth value object 
    Stores the token and expiration_time
  '''
  def __init__(self, token: str, expiration_time: str):
    self._token = token
    self._expiration_time = expiration_time

  @property
  def token(self) -> str :
    ''' token getter '''
    return self._token
  
  @property
  def expiration_time(self) -> str :
    ''' expiration_time getter '''
    return self._expiration_time
