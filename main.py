from contextlib import asynccontextmanager

import uvicorn

from database import create_tables, drop_tables
from fastapi import FastAPI
from crud import users_router
from crud import transactions_router

@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await drop_tables()
   print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(transactions_router)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
