from datetime import date

from pydantic import BaseModel


class DebtorModel(BaseModel):
    id: int
    name: str
    date_added: date


class IncompleteDebtorModel(BaseModel):
    id: int | None = None
    name: str | None = None
    date_added: date | None = None
