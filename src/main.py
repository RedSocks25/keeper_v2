import argparse
import json

from typing import Union

from config import parser
from models import User
from constants import paths


def check_user(username: str) -> bool:
  # Find the username at ./src/database/users.json
  with open(paths['USERS_DB'], 'r') as users_json:
    users: dict = json.load(users_json)['users']
  
  # Check if the username exists in users
  for user in users:
    if user['username'] == username:
      return User(**user)
  return None


def login(username: str) -> Union[User, None]:
  # Find the username at ./src/database/users.json
  user: User = check_user(username)
  if not user:
    return None
  
  while True:
    password = input(f'Enter the password for {username}: ')
    if password == user['password']:
      print(f'Welcome back, {username}!')
      return user
    print('Incorrect password. Please try again or click [Ctrl + C] to.')
    

def main():
  args = parser.parse_args()
  
  if args.login:
    print(login(args.login))
  
  return None


if __name__ == "__main__":
  main()
