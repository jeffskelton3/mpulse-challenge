import sqlalchemy as sa

from src.member.models import Member, MemberBody
from sqlalchemy.dialects import postgresql
from src.db.db import get_session


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
    member_list = __dedupe_member_list(members)
    insert_statement = postgresql.insert(Member).values(member_list)
    update_columns = {col.name: col for col in insert_statement.excluded if
                      col.name not in ['client_member_id']}
    upsert_statement = insert_statement.on_conflict_do_update(
        index_elements=['client_member_id'],
        set_=update_columns
    )
    with get_session() as session:
        session.execute(upsert_statement)
        session.commit()


def __dedupe_member_list(members: [MemberBody]) -> [MemberBody]:
    unique_members = {}
    for member in members:
        unique_members[member.client_member_id] = member

    deduped_member_list = []
    for k, v in unique_members.items():
        deduped_member_list.append(v.dict())
    return deduped_member_list
