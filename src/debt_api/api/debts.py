from typing import Annotated

from fastapi import APIRouter, Body, Query

from debt_api.services.debts import add_debt, delete_debt, get_debt, update_debt
from debt_api.services.models import DebtFilter, DebtModel, IncompleteDebtModel

router = APIRouter()


@router.get("/api/debts/")
def api_get_debt(filter: Annotated[DebtFilter, Query()]):
    return get_debt(filter)


@router.post("/api/debts/")
def api_add_debt(model: Annotated[DebtModel, Body()]):
    return add_debt(model)


@router.get("/api/debts/{id}")
def api_get_debt_by_id(id: int, filter: Annotated[DebtFilter, Query()]):
    filter.id = id
    return get_debt(filter)


@router.patch("/api/debts/{id}")
def api_update_debt(id: int, model: Annotated[IncompleteDebtModel, Body()]):
    model.id = id
    return update_debt(model)


@router.delete("/api/debts/{id}")
def api_delete_debt(id: int):
    return delete_debt(DebtFilter(id=id))
