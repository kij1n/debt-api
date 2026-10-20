from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentModel(BaseModel):
    id: int
    debtor_id: int
    amount: Decimal = Field(ge=0)
    description: str
    date_added: date


class IncompletePaymentModel(BaseModel):
    id: int | None = None
    debtor_id: int | None = None
    amount: Decimal | None = Field(None, ge=0)
    description: str | None = None
    date_added: date | None = None
