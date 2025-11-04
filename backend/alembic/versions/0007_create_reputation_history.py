"""Create reputation history table."""

from alembic import op
import sqlalchemy as sa


revision = "0007_create_reputation_history"
down_revision = "0006_create_warmup_messages"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reputation_history",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("email_accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("spam_score", sa.Float(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "ix_reputation_history_account_id",
        "reputation_history",
        ["account_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_reputation_history_account_id", table_name="reputation_history")
    op.drop_table("reputation_history")
