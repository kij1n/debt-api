from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from debt_api.db import Session
from debt_api.db.models import Debtor
from debt_api.services.models import DebtorFilter, IncompleteDebtorModel


def query_debtor(filter: DebtorFilter) -> None | Debtor | Sequence[Debtor]:
    with Session() as session:
        if filter.id is not None or filter.name is not None:
            stmt = select(Debtor)

            if filter.id is not None:
                stmt = stmt.where(Debtor.id == filter.id)

            if filter.name is not None:
                stmt = stmt.where(Debtor.name == filter.name)

            return session.scalars(stmt).first()

        stmt = select(Debtor)

        if filter.date_from is not None:
            stmt = stmt.where(Debtor.date_added >= filter.date_to)

        if filter.date_to is not None:
            stmt = stmt.where(Debtor.date_added <= filter.date_to)

        if filter.limit is not None:
            stmt = stmt.limit(filter.limit)

        if filter.offset is not None:
            stmt = stmt.offset(filter.offset)

        return session.scalars(stmt).all()

    return None


def db_add_debtor(model: IncompleteDebtorModel) -> None | Exception:
    with Session() as session:
        try:
            session.add(Debtor(**model.model_dump()))
            session.commit()
        except SQLAlchemyError as e:
            return e

    return None
