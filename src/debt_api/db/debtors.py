from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from debt_api.db import Session
from debt_api.db.models import Debtor
from debt_api.services.models import DebtorFilter, DebtorModel, IncompleteDebtorModel


def _prepare_get_stmt(filter: DebtorFilter) -> Select:
    stmt = select(Debtor)

    if filter.date_from is not None:
        stmt = stmt.where(Debtor.date_added >= filter.date_from)

    if filter.date_to is not None:
        stmt = stmt.where(Debtor.date_added <= filter.date_to)

    if filter.limit is not None:
        stmt = stmt.limit(filter.limit)

    if filter.offset is not None:
        stmt = stmt.offset(filter.offset)

    return stmt


def _prepare_exclusive_get_stmt(
    filter: DebtorFilter, wait_for_update: bool = False
) -> Select:
    stmt = select(Debtor)

    if filter.id is not None:
        stmt = stmt.where(Debtor.id == filter.id)

    if filter.name is not None:
        stmt = stmt.where(Debtor.name == filter.name)

    if wait_for_update:
        stmt = stmt.with_for_update()

    return stmt


def db_query_debtor(filter: DebtorFilter) -> None | Debtor | Sequence[Debtor]:
    with Session() as session:
        if filter.id is not None or filter.name is not None:
            stmt = _prepare_exclusive_get_stmt(filter)
            return session.scalars(stmt).first()

        stmt = _prepare_get_stmt(filter)
        return session.scalars(stmt).all()

    return None


def db_add_debtor(model: DebtorModel) -> None | Exception:
    with Session() as session:
        try:
            session.add(Debtor(**model.model_dump()))
            session.commit()
        except SQLAlchemyError as e:
            return e

    return None


def db_update_debtor(model: IncompleteDebtorModel) -> str | Exception | DebtorModel:
    with Session() as session:
        try:
            print(f"id: {model.id}, name: {model.name}")
            stmt = _prepare_exclusive_get_stmt(
                DebtorFilter(id=model.id), wait_for_update=True
            )
            debtor = session.scalars(stmt).one()

            if model.name:
                debtor.name = model.name

            if model.date_added:
                debtor.date_added = model.date_added

            session.commit()

            return DebtorModel(
                id=debtor.id, name=debtor.name, date_added=debtor.date_added
            )

        except SQLAlchemyError as e:
            return e
