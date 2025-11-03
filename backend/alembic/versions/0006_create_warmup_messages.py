"""Create warmup messages table for spam diagnostics."""

from alembic import op
import sqlalchemy as sa


revision = "0006_create_warmup_messages"
down_revision = "0005_add_warmup_mode_to_email_accounts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "warmup_messages",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("email_accounts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("activity_id", sa.Integer(), sa.ForeignKey("warmup_activities.id", ondelete="SET NULL"), nullable=True),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("spam_score", sa.Float(), nullable=True),
        sa.Column("spam_details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "ix_warmup_messages_account_id",
        "warmup_messages",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        "ix_warmup_messages_domain",
        "warmup_messages",
        ["domain"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_warmup_messages_domain", table_name="warmup_messages")
    op.drop_index("ix_warmup_messages_account_id", table_name="warmup_messages")
    op.drop_table("warmup_messages")
