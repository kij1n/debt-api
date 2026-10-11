from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DebtDireciton(Enum):
    LENT: str = "lent"
    BORROWED: str = "borrowed"


class Debt(Base):
    __tablename__ = "debt"

    id: Mapped[int] = mapped_column(primary_key=True)
    debtor_name: Mapped[str] = mapped_column(String(50))
    amount: Mapped[Decimal]
    description: Mapped[str] = mapped_column(String(300))
    direction: Mapped[DebtDireciton]
    date_added: Mapped[date] = mapped_column(default=date())
    date_settled: Mapped[date | None] = mapped_column(nullable=True)


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    debtor_id: Mapped[int]
    amount: Mapped[Decimal]
    description: Mapped[str]
    date_added: Mapped[date]


class Allocation(Base):
    pass


class Debtor(Base):
    pass
