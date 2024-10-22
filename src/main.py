import argparse
import json

from typing import Union
from pprint import pprint

from config import parser
from models import User, Account
from classes import AccountsLedger
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


def load_accounts_to_hash_table(accounts: list[dict]) -> dict[str, list[Account]]:

  accounts_hash_table: dict[str, list[Account]] = {}

  for account in accounts:
    platform = account['platform']
    if platform in accounts_hash_table:
      accounts_hash_table[platform].append(Account(**account))
    else:
      accounts_hash_table[platform] = [Account(**account)]

  return accounts_hash_table


def login(username: str) -> AccountsLedger:
  # Find the username at ./src/database/users.json
  user: User = check_user(username)
  if not user:
    return None
  
  while True:
    password = input(f'Enter the password for {username}: ')

    if password == user['password']:
      break
    else:
      print('Incorrect password. Please try again or click [Ctrl + C] to.')
    
  user_accounts: dict = load_accounts_to_hash_table(user['accounts'])

  return AccountsLedger(user['username'], user_accounts)
    
  
def main():
  ledger: Union[AccountsLedger | None] = None
  
  args = parser.parse_args()

  if args.login:
    ledger: AccountsLedger = login(args.login)
  
  if not ledger:
    print('User not found. Exiting...')
    return None
  
  while True:
    print('Welcome to the Accounts Ledger')
    print('Choose an option:')
    print('1. List all accounts')
    print('2. List accounts by platform')
    print('3. Add an account')
    print('4. Remove an account')
    print('5. Exit')
    option = input('Enter your choice: ')
    
    if option == '1':
      ledger.show_all_accounts()
    elif option == '2':
      platform = input('Enter the platform: ')
      if platform in ledger.accounts:
        pprint(ledger.accounts[platform])
      else:
        print('No accounts found for this platform')
    elif option == '3':
      platform = input('Enter the platform: ')
      username = input('Enter the username: ')
      password = input('Enter the password: ')
      email = input('Enter the email: ')
      account = Account(platform=platform, username=username, password=password, email=email)
      if platform in ledger.accounts:
        ledger.accounts[platform].append(account)
      else:
        ledger.accounts[platform] = [account]
    elif option == '4':
      platform = input('Enter the platform: ')
      username = input('Enter the username: ')
      for account in ledger.accounts[platform]:
        if account.username == username:
          ledger.accounts[platform].remove(account)
          break
    elif option == '5':
      print('Exiting...')
      break
    else:
      print('Invalid option. Please try again.')
  
  return None


if __name__ == "__main__":
  main()
