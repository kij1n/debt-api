from decimal import Decimal

from pydantic import BaseModel, Field


class AllocationModel(BaseModel):
    payment_id: int
    debt_id: int
    amount: Decimal = Field(gt=0)


class IncompleteAllocationModel(BaseModel):
    payment_id: int | None = None
    debt_id: int | None = None
    amount: Decimal | None = Field(None, gt=0)
