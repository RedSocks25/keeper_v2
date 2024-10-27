import json
from getpass import getpass

from constants.paths import paths
from models.user import User


def find_user(username: str) -> User:
  """
  Find the username at the local JSON database

  Args:
    username (str): The username to find
  
  Returns:
    User: The user object if found, None otherwise
  """
  with open(paths['USERS_DB'], 'r') as users_json:
    users: dict = json.load(users_json)['users']
  
  for user in users:
    if user['username'] == username:
      return User(**user)
  
  return None


def login(username: str) -> User:
  """
  Login the user into the system

  Args:
    username (str): The username to login
  
  Returns:
    User: The user object if found, None otherwise
  """
  user: User = find_user(username)
  if not user:
    return None

  while True:
    password: str = getpass(f'Enter {username}\'s password: ')
    if password == user['password']:
      break
    else:
      print('Invalid password. Please try again or press [Ctrl + C] to exit.')
    
  return user