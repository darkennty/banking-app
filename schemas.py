from datetime import date
from pydantic import BaseModel

class UserAdd(BaseModel):
    name: str
    surname: str
    patronymic: str
    birth_date: date
    balance: float

class User(UserAdd):
    user_id: int

class UserId(BaseModel):
    ok: bool = True
    user_id: int

class UserGet(BaseModel):
    user_id: int

class UserBalanceChange(BaseModel):
    user_id: int
    balance: float

class UserDataChange(BaseModel):
    user_id: int
    name: str
    surname: str
    patronymic: str
    birth_date: date


class TransactionAdd(BaseModel):
    user_from_id: int
    user_to_id: int
    amount: float

class Transaction(TransactionAdd):
    transaction_id: int

class TransactionId(BaseModel):
    ok: bool = True
    transaction_id: int

class TransactionGet(BaseModel):
    transaction_id: int