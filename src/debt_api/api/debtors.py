from typing import Annotated

from fastapi import APIRouter, Body, Query

from debt_api.services.debtors import add_debtor, get_debtor, update_debtor
from debt_api.services.models import DebtorFilter, DebtorModel, IncompleteDebtorModel

router = APIRouter()


@router.get("/api/debtor/")
def api_get_debtor(filter: Annotated[DebtorFilter, Query()]):
    return get_debtor(filter)


@router.post("/api/debtor/")
def api_add_debtor(body: Annotated[DebtorModel, Body()]):
    return add_debtor(model=body)


@router.get("/api/debtor/{id}")
def api_get_debtor_by_id(id: int):
    return get_debtor(DebtorFilter(id=id))


@router.patch("/api/debtor/{id}")
def api_update_debtor_by_id(id: int, body: Annotated[IncompleteDebtorModel, Body()]):
    body.id = id
    return update_debtor(body)


@router.delete("/api/debtor/{id}")
def api_delete_debtor_by_id(id: int):
    pass
