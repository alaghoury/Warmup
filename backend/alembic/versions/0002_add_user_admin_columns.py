"""Ensure user auth columns exist."""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_user_admin_columns"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    if not _has_column("users", "hashed_password"):
        op.add_column(
            "users",
            sa.Column("hashed_password", sa.String(length=255), nullable=True, server_default=""),
        )
        op.execute("UPDATE users SET hashed_password = '' WHERE hashed_password IS NULL")
        op.alter_column("users", "hashed_password", nullable=False, server_default=None)

    if not _has_column("users", "is_admin"):
        op.add_column(
            "users",
            sa.Column("is_admin", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        )
        op.execute("UPDATE users SET is_admin = 0 WHERE is_admin IS NULL")
        op.alter_column("users", "is_admin", nullable=False, server_default=sa.text("0"))

    if not _has_column("users", "is_active"):
        op.add_column(
            "users",
            sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.text("1")),
        )
        op.execute("UPDATE users SET is_active = 1 WHERE is_active IS NULL")
        op.alter_column("users", "is_active", nullable=False, server_default=sa.text("1"))



def downgrade() -> None:
    if _has_column("users", "is_active"):
        op.drop_column("users", "is_active")
    if _has_column("users", "is_admin"):
        op.drop_column("users", "is_admin")
    if _has_column("users", "hashed_password"):
        op.drop_column("users", "hashed_password")
