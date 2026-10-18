from sqlalchemy import and_, select

from debt_api.db import Session
from debt_api.db.models import Debtor
from debt_api.services.models import IncompleteDebtor


def get_debtor(filter: IncompleteDebtor) -> Debtor | list[Debtor]:
    with Session() as session:
        if filter.id is not None:
            stmt = select(Debtor).where(Debtor.id == filter.id)
            return session.scalars(stmt).first()

        stmt = select(Debtor).filter(
            and_(Debtor.name == filter.name if filter.name is not None else True),
            and_(
                Debtor.date_added == filter.date_added
                if filter.date_added is not None
                else True
            ),
        )
        return session.scalars(stmt).all()
