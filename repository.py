from sqlalchemy import select, update, delete

from database import new_session, TransactionTable, UserTable
from schemas import TransactionAdd, UserAdd, User, Transaction


class TransactionRepository:
    @classmethod
    async def get_one(cls, tr_id) -> list[Transaction]:
        async with new_session() as session:
            query = select(TransactionTable).where(TransactionTable.transaction_id == tr_id)
            result = await session.execute(query)
            transaction_models = result.scalars().all()
            return transaction_models


    @classmethod
    async def add(cls, data: TransactionAdd):
        async with new_session() as session:
            user_from = await UserRepository.get_one(data.user_from_id)

            if not user_from:
                return {"ok": False, "error_code": -1, "msg": "No such user in the system"}
            elif user_from[0].balance < data.amount:
                return {"ok": False, "error_code": -2, "msg": "Not enough funds"}

            user_to = await UserRepository.get_one(data.user_to_id)

            if not user_to:
                return {"ok": False, "error_code": -1, "msg": "No such user in the system"}

            transaction_dict = data.model_dump()

            transaction = TransactionTable(**transaction_dict)
            session.add(transaction)

            query = update(UserTable).where(UserTable.user_id == data.user_from_id).values(
                balance=UserTable.balance - data.amount
            )
            await session.execute(query)

            query = update(UserTable).where(UserTable.user_id == data.user_to_id).values(
                balance=UserTable.balance + data.amount
            )
            await session.execute(query)

            await session.flush()
            await session.commit()
            return {"ok": True, "transaction_id": transaction.transaction_id}


    @classmethod
    async def get_all(cls) -> list[Transaction]:
        async with new_session() as session:
            query = select(TransactionTable)
            result = await session.execute(query)
            transaction_models = result.scalars().all()
            return transaction_models



class UserRepository:
    @classmethod
    async def add(cls, data: UserAdd) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()

            user = UserTable(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.user_id

    @classmethod
    async def get_one(cls, u_id):
        async with new_session() as session:
            query = select(UserTable).where(UserTable.user_id == u_id)
            result = await session.execute(query)
            user_models = result.scalars().all()
            return user_models

    @classmethod
    async def get_all(cls) -> list[User]:
        async with new_session() as session:
            query = select(UserTable)
            result = await session.execute(query)
            user_models = result.scalars().all()
            return user_models

    @classmethod
    async def update_balance(cls, u_id, new_balance):
        async with new_session() as session:
            query = update(UserTable).where(UserTable.user_id == u_id).values(balance=new_balance)
            await session.execute(query)
            await session.flush()
            await session.commit()

    @classmethod
    async def update_user_data(cls, user):
        async with new_session() as session:
            query = update(UserTable).where(UserTable.user_id == user.user_id).values(
                name=user.name,
                surname=user.surname,
                patronymic=user.patronymic,
                birth_date=user.birth_date
            )
            await session.execute(query)
            await session.flush()
            await session.commit()

    @classmethod
    async def delete_user(cls, user):
        async with new_session() as session:
            query = delete(UserTable).where(UserTable.user_id == user.user_id)
            await session.execute(query)
            await session.flush()
            await session.commit()