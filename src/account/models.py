import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import sqlalchemy as sa

from src.db.db import Base


class Account(Base):
    __tablename__ = "account"
    account_id = sa.Column("account_id", sa.INTEGER, primary_key=True)


class MemberAccount(Base):
    __tablename__ = "member_account"
    member_account_id = sa.Column(
        "member_account_id",
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
    )
    account_id = sa.Column(
        "account_id", sa.INTEGER, ForeignKey("account.account_id", ondelete="CASCADE")
    )
    member_id = sa.Column(
        "member_id",
        UUID(as_uuid=True),
        ForeignKey("member.member_id", ondelete="CASCADE"),
    )


class MemberAccountBody(BaseModel):
    account_id: int
    client_member_id: str


class AccountBody(BaseModel):
    account_id: int
