from debt_api.db.debtors import db_add_debtor, query_debtor
from debt_api.db.models import Debtor
from debt_api.services.models import IncompleteDebtorModel


def get_debtor(filter: IncompleteDebtorModel) -> Debtor | list[Debtor]:
    return query_debtor(filter)


def add_debtor(model: IncompleteDebtorModel) -> None | Exception | str:
    if type(get_debtor(filter=model)) in [Debtor, list[Debtor]]:
        return "Debtor aleady exists"
    return db_add_debtor(model)
