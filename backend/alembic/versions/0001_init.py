"""Initial schema for Warmup SaaS.

Revision ID: 0001_init
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=32), server_default=sa.text("'active'"), nullable=False),
    )

    op.create_table(
        "warming_tasks",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=32), server_default=sa.text("'email'"), nullable=False),
        sa.Column("state", sa.String(length=32), server_default=sa.text("'queued'"), nullable=False),
    )
    op.create_index("ix_warming_tasks_account_id", "warming_tasks", ["account_id"])


def downgrade() -> None:
    op.drop_index("ix_warming_tasks_account_id", table_name="warming_tasks")
    op.drop_table("warming_tasks")
    op.drop_table("accounts")
    op.drop_table("users")
