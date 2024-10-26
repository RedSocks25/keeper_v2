import argparse
import json
import os

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


def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')


def login(username: str) -> AccountsLedger:
  # Find the username at ./src/database/users.json
  user: User = check_user(username)
  if not user:
    return None
  
  print(f'Welcome to your accounts ledger, {username}!')
  
  while True:
    password = input(f'Enter the password for {username}: ')

    if password == user['password']:
      break
    else:
      print('Incorrect password. Please try again or click [Ctrl + C] to.')
    
  user_accounts: dict = load_accounts_to_hash_table(user['accounts'])

  return AccountsLedger(user['username'], user_accounts)
    
  
def main():
  clear_console()
  args = parser.parse_args()
  
  ledger: Union[AccountsLedger | None] = None
  
  if args.login:
    ledger: AccountsLedger = login(args.login)
  
  if not ledger:
    print('User not found. Exiting...')
    return None
  
  clear_console()
  
  while True:
    print(f"--- {ledger.username}'s Accounts Ledger ---\n")
    print('1. List all accounts')
    print('2. List accounts by platform')
    print('3. Add an account')
    print('4. Edit an account')
    print('5. Remove an account')
    print('6. Exit')
    option = input('\nEnter your choice: ')

    clear_console()
    
    # Show all accounts
    if option == '1':
      ledger.show_all_accounts()

    # Show accounts by platform given
    elif option == '2':
      platform = input('Enter the platform: ')
      ledger.show_platform_accounts(platform)
    
    # Add an account
    elif option == '3':
      ledger.add_account()
    
    # Edit an account
    elif option == '4':
      platform = input('Enter the platform: ')
      ledger.edit_account(platform)

    # Remove an account
    elif option == '5':
      platform = input('Enter the platform: ')      
      ledger.remove_account(platform)

    # Exit
    elif option == '6':
      print('Exiting...')
      break
    else:
      print('Invalid option. Please try again.')
    
    # Wait until user presses enter
    input('\nPress [Enter] to continue...')
    clear_console()
  
  return None


if __name__ == "__main__":
  main()
