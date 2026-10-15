from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class Pagination(BaseModel):
    limit: int = Field(50, ge=1, le=200)
    offset: int = Field(0, ge=0)


class DateRange(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class AmountRange(BaseModel):
    amount_min: Decimal | None = Field(None, ge=0)
    amount_max: Decimal | None = Field(None, ge=0)


class PaymentFilter(Pagination, DateRange, AmountRange):
    model_config = ConfigDict(extra="forbid")
    debtor_id: int | None = None


class DebtFilter(Pagination, DateRange, AmountRange):
    model_config = ConfigDict(extra="forbid")
    debtor_id: int | None = None


class DebtorFilter(Pagination, DateRange):
    model_config = ConfigDict(extra="forbid")
