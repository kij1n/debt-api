from typing import Annotated

from fastapi import APIRouter, Body, Query

from debt_api.services.debtors import add_debtor, get_debtor
from debt_api.services.models import DebtorFilter, IncompleteDebtorModel

router = APIRouter()


@router.get("/api/debtor/")
def api_get_debtor(filter: Annotated[DebtorFilter, Query()]):
    return get_debtor(filter)


@router.post("/api/debtor/")
def api_add_debtor(body: Annotated[IncompleteDebtorModel, Body()]):
    return add_debtor(model=body)
