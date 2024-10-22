from dataclasses import dataclass


@dataclass
class AccountsLedger:

  def __init__(self, username: str, accounts: {}):
    self.username = username
    self.accounts = accounts # Hashmap of accounts
  
  def show_all_accounts(self):
    for platform, accounts in self.accounts.items():
      print(f'Platform: {platform}')
      for account in accounts:
        print(f'Username: {account['username']}')
        print(f'Password: {account['password']}')
        print(f'Email: {account['email']}')
        print()
  

