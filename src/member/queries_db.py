import sqlalchemy as sa

from src.member.models import Member, MemberBody
from sqlalchemy.dialects import postgresql
from src.db.db import get_session
from src.utils.list_helpers import unique_basemodel_list


def get_members():
    statement = sa.select(Member).filter()
    with get_session() as session:
        result = session.execute(statement)
        return result.scalars().all()


def find_member_by_client_member_id(client_member_id: str):
    statement = sa.select(Member).filter(Member.client_member_id == client_member_id)
    with get_session() as session:
        result = session.execute(statement)
        return result.scalars().one_or_none()


def find_by_id(member_id: str):
    statement = sa.select(Member).filter(Member.member_id == member_id)
    with get_session() as session:
        result = session.execute(statement)
        return result.scalars().one_or_none()


def add_member(member: MemberBody):
    upsert_members([member])


def upsert_members(members: [MemberBody]) -> None:
    member_list = unique_basemodel_list(members, "client_member_id")
    insert_statement = postgresql.insert(Member).values(member_list)
    update_columns = {col.name: col for col in insert_statement.excluded if
                      col.name not in ['client_member_id', 'member_id']}
    upsert_statement = insert_statement.on_conflict_do_update(
        index_elements=['client_member_id'],
        set_=update_columns
    )
    with get_session() as session:
        session.execute(upsert_statement)
        session.commit()
