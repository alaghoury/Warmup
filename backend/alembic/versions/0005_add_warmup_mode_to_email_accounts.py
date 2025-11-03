"""Add warmup_mode column to email accounts."""

from alembic import op
import sqlalchemy as sa


revision = "0005_add_warmup_mode_to_email_accounts"
down_revision = "0004_add_email_accounts"
branch_labels = None
depends_on = None


warmup_enum = sa.Enum("growth", "flat", "random", name="warmup_mode")


def upgrade() -> None:
    bind = op.get_bind()
    warmup_enum.create(bind, checkfirst=True)
    op.add_column(
        "email_accounts",
        sa.Column(
            "warmup_mode",
            warmup_enum,
            nullable=False,
            server_default="growth",
        ),
    )
    op.alter_column("email_accounts", "warmup_mode", server_default=None)


def downgrade() -> None:
    op.drop_column("email_accounts", "warmup_mode")
    bind = op.get_bind()
    warmup_enum.drop(bind, checkfirst=True)
