from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import sqlalchemy as sa

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"
    account_id = sa.Column("account_id", sa.INTEGER, primary_key=True)


class MemberAccount(Base):
    __tablename_ = "member_account"
    member_account_ID = sa.Column("member_account_id", sa.INTEGER, primary_key=True, autoincrement=True)
    account_id = sa.Column("account_id", sa.INTEGER, foreign_keys="Account.account_id")
    member_id = sa.Column("member_id", sa.INTEGER, foreign_keys="Member.member_id")
