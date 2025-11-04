"""Create warmup activities table."""

from alembic import op
import sqlalchemy as sa


revision = "0003_create_warmup_activity"
down_revision = "0002_add_user_admin_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "warmup_activities",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("step", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("details", sa.JSON(), nullable=True),
    )
    op.create_index(
        "ix_warmup_activities_timestamp",
        "warmup_activities",
        ["timestamp"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_warmup_activities_timestamp", table_name="warmup_activities")
    op.drop_table("warmup_activities")
