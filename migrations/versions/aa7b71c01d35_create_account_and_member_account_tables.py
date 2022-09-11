"""create account and member account tables

Revision ID: aa7b71c01d35
Revises: 9a1f49a7045e
Create Date: 2022-09-07 21:49:35.961044

"""
import uuid

from alembic import op
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'aa7b71c01d35'
down_revision = '9a1f49a7045e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'account',
        Column("account_id", Integer, index=True, primary_key=True)
    )
    op.create_table(
        'member_account',
        Column("member_account_id", UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4),
        Column("account_id", Integer, index=True),
        Column("member_id", UUID(as_uuid=True), unique=True),
    )
    op.create_foreign_key(
        constraint_name="fk_account",
        source_table="member_account",
        referent_table="account",
        local_cols=["account_id"],
        remote_cols=["account_id"])

    op.create_foreign_key(
        constraint_name="fk_member",
        source_table="member_account",
        referent_table="member",
        local_cols=["member_id"],
        remote_cols=["member_id"])


def downgrade() -> None:
    op.drop_constraint("fk_account", 'member_account', type_='foreignkey')
    op.drop_constraint("fk_member", 'member_account', type_='foreignkey')
    op.drop_table('account')
    op.drop_table('member_account')
