from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from debt_api.db import Session


def is_healthy() -> bool:
    with Session() as session:
        try:
            session.scalars(text("SELECT 1"))
        except OperationalError:
            return False

        return True
