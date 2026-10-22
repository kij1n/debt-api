from collections.abc import Sequence

from debt_api.db.debtors import db_add_debtor, db_query_debtor, db_update_debtor
from debt_api.db.models import Debtor
from debt_api.services.models import DebtorFilter, DebtorModel, IncompleteDebtorModel


def get_debtor(filter: DebtorFilter) -> None | Debtor | Sequence[Debtor]:
    return db_query_debtor(filter)


def add_debtor(model: DebtorModel) -> None | Exception | str:
    if type(get_debtor(filter=DebtorFilter(name=model.name))) in [Debtor, list[Debtor]]:
        return "Debtor aleady exists."
    return db_add_debtor(model)


def update_debtor(model: IncompleteDebtorModel) -> str | Exception | DebtorModel:
    if model.id is None:
        return "No id given."
    return db_update_debtor(model)
