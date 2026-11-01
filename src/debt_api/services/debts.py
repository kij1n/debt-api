from debt_api.db.debts import db_add_debt, db_query_debt, db_remove_debt, db_update_debt
from debt_api.services.models import DebtFilter, DebtModel, IncompleteDebtModel


def get_debt(filter: DebtFilter):
    return db_query_debt(filter)


def add_debt(model: DebtModel):
    return db_add_debt(model)


def update_debt(model: IncompleteDebtModel):
    if db_query_debt(DebtFilter(id=model.id)) is None:
        return "No debt with this id."

    return db_update_debt(model)


def delete_debt(filter: DebtFilter):
    if db_query_debt(DebtFilter(id=filter.id)):
        return "No debt with this id."

    return db_remove_debt(filter)
