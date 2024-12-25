from typing import Annotated

from fastapi import APIRouter, Depends

from repository import TransactionRepository, UserRepository
from schemas import *

users_router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
)

transactions_router = APIRouter(
    prefix="/transaction",
    tags=["Транзакции"]
)

### CREATE
@users_router.post("", summary="Добавить пользователя")
async def add_user(
    user: Annotated[UserAdd, Depends()]
) -> UserId:
    user_id = await UserRepository.add(user)
    return {"ok": True, "user_id": user_id}

@transactions_router.post("", summary="Добавить транзакцию")
async def add_transaction(
    transaction: Annotated[TransactionAdd, Depends()]
):
    task = await TransactionRepository.add(transaction)
    if task["ok"]:
        return {"ok": task["ok"], "transaction_id": task["transaction_id"]}
    else:
        return {"ok": task["ok"], "error_code": task["error_code"], "msg": task["msg"]}


### READ

@users_router.get("/one", summary="Получить одного пользователя")
async def get_one_user(
    user: Annotated[UserGet, Depends()]
) -> list[User]:
    users = await UserRepository.get_one(user.user_id)
    return users

@users_router.get("/all", summary="Получить всех пользователей")
async def get_all_users() -> list[User]:
    users = await UserRepository.get_all()
    return users

@transactions_router.get("/one", summary="Получить одну транзакцию")
async def get_one_transaction(
    transaction: Annotated[TransactionGet, Depends()]
) -> list[Transaction]:
    transactions = await TransactionRepository.get_one(transaction.transaction_id)
    return transactions

@transactions_router.get("/all", summary="Получить все транзакции")
async def get_all_transactions() -> list[Transaction]:
    transactions = await TransactionRepository.get_all()
    return transactions

### UPDATE

@users_router.put("/balance", summary="Изменить баланс пользователя")
async def update_user_balance(
    user: Annotated[UserBalanceChange, Depends()]
):
    await UserRepository.update_balance(user.user_id, user.balance)
    return True

@users_router.put("/data", summary="Изменить данные пользователя")
async def update_user_balance(
    user: Annotated[UserDataChange, Depends()]
):
    await UserRepository.update_user_data(user)
    return True

### DELETE

@users_router.delete("", summary="Удалить пользователя")
async def delete_one_user(
        user: Annotated[UserGet, Depends()]
):
    await UserRepository.delete_user(user)
    return True