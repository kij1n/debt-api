from fastapi import FastAPI

from debt_api.api.debtors import router as debtor_router
from debt_api.api.main import router as main_router

app = FastAPI()
app.include_router(debtor_router)
app.include_router(main_router)
