from typing import TypedDict


class Account(TypedDict):
  platform: str
  username: str
  password: str
  email:    str

class User(TypedDict):
  username: str
  password: str
  accounts: list[Account]
