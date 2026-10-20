from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from debt_api.db.models import DebtDireciton


class DebtModel(BaseModel):
    id: int
    batch_id: int | None = None
    debtor_name: int
    amount: Decimal = Field(ge=0)
    description: str
    direction: DebtDireciton
    date_added: date
    date_settled: date


class IncompleteDebtModel(BaseModel):
    id: int | None = None
    batch_id: int | None = None
    debtor_name: int
    amount: Decimal | None = Field(None, ge=0)
    description: str | None = None
    direction: DebtDireciton | None = None
    date_added: date | None = None
    date_settled: date | None = None
