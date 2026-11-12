"""Initial generation

Revision ID: b408c3a0a161
Revises:
Create Date: 2026-11-12 17:06:09.939006

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b408c3a0a161"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "debtor",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("date_added", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "debt",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("debtor_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("description", sa.String(length=300), nullable=False),
        sa.Column(
            "direction",
            sa.Enum("LENT", "BORROWED", name="debtdireciton"),
            nullable=False,
        ),
        sa.Column("date_added", sa.Date(), nullable=False),
        sa.Column("date_settled", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["debtor_id"],
            ["debtor.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "payment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("debtor_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("description", sa.String(length=300), nullable=False),
        sa.Column("date_added", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["debtor_id"],
            ["debtor.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "allocation",
        sa.Column("payment_id", sa.Integer(), nullable=False),
        sa.Column("debt_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["debt_id"],
            ["debt.id"],
        ),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payment.id"],
        ),
        sa.PrimaryKeyConstraint("payment_id", "debt_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("allocation")
    op.drop_table("payment")
    op.drop_table("debt")
    op.drop_table("debtor")
