from typing import Annotated

from fastapi import APIRouter, Query

from debt_api.services.debtors import get_debtor
from debt_api.services.models import IncompleteDebtorModel

router = APIRouter()


@router.get("/api/debtor/")
def api_get_debtor(filter: Annotated[IncompleteDebtorModel, Query()]):
    return get_debtor(filter)
