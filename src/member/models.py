import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import sqlalchemy as sa

Base = declarative_base()


class Member(Base):
    __tablename__ = "member"
    member_id = sa.Column("member_id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    client_member_id = sa.Column("client_member_id", sa.VARCHAR, unique=True, nullable=False)
    first_name = sa.Column("first_name", sa.VARCHAR, nullable=False)
    last_name = sa.Column("last_name", sa.VARCHAR, nullable=False)
    phone_number = sa.Column("phone_number", sa.VARCHAR, nullable=False)


class MemberBody(BaseModel):
    client_member_id: str
    first_name: str
    last_name: str
    phone_number: str
