"""Add email accounts table."""

from alembic import op
import sqlalchemy as sa


revision = "0004_add_email_accounts"
down_revision = "0003_create_warmup_activity"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "email_accounts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("access_token", sa.String(length=512), nullable=True),
        sa.Column("refresh_token", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ix_email_accounts_user_id",
        "email_accounts",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_email_accounts_email",
        "email_accounts",
        ["email"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_email_accounts_email", table_name="email_accounts")
    op.drop_index("ix_email_accounts_user_id", table_name="email_accounts")
    op.drop_table("email_accounts")
