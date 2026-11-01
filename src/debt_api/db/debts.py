from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.exc import SQLAlchemyError

from debt_api.db import Session
from debt_api.db.models import Debt
from debt_api.services.models import DebtFilter, DebtModel, IncompleteDebtModel


def _get_debt_stmt(filter: DebtFilter):
    stmt = Select(Debt)

    if filter.amount_min is not None:
        stmt = stmt.where(Debt.amount >= filter.amount_min)
    if filter.amount_max is not None:
        stmt = stmt.where(Debt.amount <= filter.amount_max)
    if filter.date_from is not None:
        stmt = stmt.where(Debt.date_added >= filter.date_from)
    if filter.date_to is not None:
        stmt = stmt.where(Debt.date_added <= filter.date_to)
    if filter.debtor_id is not None:
        stmt = stmt.where(Debt.debtor_id == filter.debtor_id)

    if filter.limit is not None:
        stmt = stmt.limit(filter.limit)
    if filter.offset is not None:
        stmt = stmt.offset(filter.offset)

    return stmt


def db_query_debt(filter: DebtFilter) -> None | Debt | Sequence[Debt]:
    with Session() as session:
        stmt = _get_debt_stmt(filter)
        try:
            debts = session.scalars(stmt)
            return debts.all()
        except SQLAlchemyError:
            return None

    return None


def db_add_debt(model: DebtModel):
    with Session() as session:
        try:
            session.add(Debt(**model.model_dump()))
            session.commit()
        except SQLAlchemyError as e:
            return e

    return None


def db_remove_debt(filter: DebtFilter) -> None | Exception:
    with Session() as session:
        try:
            stmt = _get_debt_stmt(filter)
            debts = session.scalars(stmt).all()

            if type(debts) == Debt:
                session.delete(debts)
            else:
                for debt in debts:
                    session.delete(debt)

            session.commit()
        except SQLAlchemyError as e:
            return e

    return None


def db_update_debt(model: IncompleteDebtModel) -> str | Exception | DebtModel:
    with Session() as session:
        try:
            stmt = _get_debt_stmt(DebtFilter(id=model.id))
            debt: Debt = session.scalars(stmt).one()

            for name, val in vars(model).items():
                if val is not None and hasattr(debt, name):
                    setattr(debt, name, val)

            session.commit()
            return DebtModel.model_validate(debt)

        except SQLAlchemyError as e:
            return e
