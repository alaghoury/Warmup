"""initial tables

Revision ID: 0001_init
Revises: 
Create Date: 2025-10-27 15:16:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

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
    op.create_index("ix_warming_tasks_account_id", "warming_tasks", ["account_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_warming_tasks_account_id", table_name="warming_tasks")
    op.drop_table("warming_tasks")
    op.drop_table("accounts")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
