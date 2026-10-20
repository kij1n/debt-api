from datetime import date
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DebtDireciton(StrEnum):
    LENT: str = "lent"
    BORROWED: str = "borrowed"


class Debt(Base):
    __tablename__ = "debt"

    id: Mapped[int] = mapped_column(primary_key=True)
    debtor_id: Mapped[str] = mapped_column(ForeignKey("debtor.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    description: Mapped[str] = mapped_column(String(300))
    direction: Mapped[DebtDireciton]
    date_added: Mapped[date] = mapped_column(default=date.today)
    date_settled: Mapped[date | None] = mapped_column(nullable=True)

    debtor: Mapped["Debtor"] = relationship(back_populates="debts")


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    debtor_id: Mapped[int] = mapped_column(ForeignKey("debtor.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    description: Mapped[str] = mapped_column(String(300))
    date_added: Mapped[date] = mapped_column(default=date.today)


class Allocation(Base):
    __tablename__ = "allocation"

    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), primary_key=True)
    debt_id: Mapped[int] = mapped_column(ForeignKey("debt.id"), primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))


class Debtor(Base):
    __tablename__ = "debtor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    date_added: Mapped[date] = mapped_column(default=date.today)

    debts: Mapped[list["Debt"]] = relationship(back_populates="debtor")
