"""create members table

Revision ID: 9a1f49a7045e
Revises: 
Create Date: 2022-09-04 21:57:20.323986

"""
import uuid

from alembic import op
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '9a1f49a7045e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'member',
        Column("member_id", UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid.uuid4),
        Column("client_member_id", String(50), index=True, unique=True, nullable=False),
        Column("first_name", String(100), nullable=False),
        Column("last_name", String(100), nullable=False),
        Column("phone_number", String(50), index=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('member')
