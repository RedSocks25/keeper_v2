import argparse
import json
import os

from typing import Union
from pprint import pprint

from config import parser
from models import User, Account
from classes import AccountsLedger
from constants import paths
from utils import login


# TODO: Add docstrings to the functions

def hash_accounts(accounts: list[dict]) -> dict[str, list[Account]]:
  accounts_hash_table: dict[str, list[Account]] = {}

  for account in accounts:
    platform = account['platform']
    if platform in accounts_hash_table:
      accounts_hash_table[platform].append(Account(**account))
    else:
      accounts_hash_table[platform] = [Account(**account)]

  return accounts_hash_table


def unhash_accounts(accounts: dict[str, list[Account]]) -> list[Account]:
  unhashed_accounts: list[Account] = []
  
  for platform, accounts_list in accounts.items():
    for account in accounts_list:
      unhashed_accounts.append(account)
  
  return unhashed_accounts
  

def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')


def save_user_accounts(username: str, accounts: dict[str, list[Account]]):
  with open(paths['USERS_DB'], 'r') as users_json:
    users: dict = json.load(users_json)['users']
  
  for user in users:
    if user['username'] == username:
      user['accounts'] = unhash_accounts(accounts)
      break
  
  with open(paths['USERS_DB'], 'w') as users_json:
    json.dump({'users': users}, users_json, indent=2)
  
  return None
    
  
def main():
  clear_console()
  args = parser.parse_args()
  
  active_user: Union[User | None] = None
  if args.login:
    active_user = login(args.login)
  
  if not active_user:
    print('User not found. Exiting...')
    return None
  
  ledger = AccountsLedger(active_user['username'], hash_accounts(active_user['accounts']))

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
      save_user_accounts(ledger.username, ledger.accounts)
    
    # Edit an account
    elif option == '4':
      platform = input('Enter the platform: ')
      ledger.edit_account(platform)
      save_user_accounts(ledger.username, ledger.accounts)

    # Remove an account
    elif option == '5':
      platform = input('Enter the platform: ')      
      ledger.remove_account(platform)
      save_user_accounts(ledger.username, ledger.accounts)
      

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
