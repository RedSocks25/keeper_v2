from dataclasses import dataclass


@dataclass
class AccountsLedger:
  """ Class to manage user accounts """

  def __init__(self, username: str, accounts: {}, db_path: str = None):
    self.username = username
    self.accounts = accounts # Hashmap of accounts
    self.db_path = db_path # Path to the user's database and manage data long-term


  # Option 1
  def show_all_accounts(self):
    print(' --- [All your accounts] --- \n')
    for platform, accounts in self.accounts.items():
      print(f'{platform} accounts')
      for i, account in enumerate(accounts):
        print(f'\t{i+1}. {account["username"]} | {account["email"]} | {account["password"]}')
      print()
  

  # Option 2
  def show_platform_accounts(self, platform: str):
    print(f' --- [{platform} related accounts] --- \n')
    platform_accounts = self.accounts.get(platform, [])
    if len(platform_accounts) == 0:
      print('No accounts found for this platform')
      return
    
    for i, account in enumerate(platform_accounts):
      print(f'{i+1}. {account["username"]} | {account["email"]} | {account["password"]}')
  

  # Option 3
  def add_account(self):
    print(' --- [Add new account] --- \n')
    platform = input('Enter the platform: ')
    email = input('Enter the email: ')
    password = input('Enter the password: ')
    username = input('Enter the username (Press [ENTER] if not): ')

    account = {
      'platform': platform,
      'username': username if username else 'no-username',
      'password': password,
      'email': email
    }

    self.accounts.setdefault(platform, []).append(account)
  

  # Option 4
  def edit_account(self, platform: str):
    print(' --- [Edit account] --- \n')
    platform_accounts = self.accounts.get(platform, [])
    if len(platform_accounts) == 0:
      print('No accounts found for this platform')
      return
    
    for i, account in enumerate(platform_accounts):
      print(f'{i+1}. {account["username"]} | {account["email"]} | {account["password"]}')
    
    # TODO: Review this code to handle invalid inputs
    choice = int(input('Enter the account number to edit: '))

    # TODO: This code should able the user to change the platform name and if so, update the hashmap key or append the account to the new platform or an existing one
    new_username = input('Enter the new username: ')
    new_password = input('Enter the new password: ')
    new_email = input('Enter the new email: ')
    
    self.accounts[platform][choice-1]['username'] = new_username
    self.accounts[platform][choice-1]['password'] = new_password
    self.accounts[platform][choice-1]['email'] = new_email

  
  # Option 5
  def remove_account(self, platform: str):
    print(' --- [Remove account] --- \n')
    platform_accounts = self.accounts.get(platform, [])
    if len(platform_accounts) == 0:
      print('No accounts found for this platform')
      return
    
    for i, account in enumerate(platform_accounts):
      print(f'{i+1}. {account["username"]} | {account["email"]} | {account["password"]}')
    
    choice = int(input('Enter the account number to delete: '))
    del self.accounts[platform][choice-1]
  
  # Save option asynchroneously in file
  def save(self):
    # TODO: Implement this method to save the accounts in a file
    pass