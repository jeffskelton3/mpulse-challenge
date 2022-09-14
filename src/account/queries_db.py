import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Result
from sqlalchemy.sql import Select

from src.account.models import MemberAccountBody, MemberAccount, AccountBody, Account
from src.db.db import get_session
from src.member.models import Member
from src.utils.list_helpers import unique_basemodel_list


def find_by_account_id(account_id: int):
    statement: Select = sa.select(Member)
    statement.join(MemberAccount, Member.member_id == MemberAccount.member_id)
    statement.where(MemberAccount.account_id == account_id)
    with get_session() as session:
        result: Result = session.execute(statement)
        return result.scalars().all()


def upsert_accounts(accounts: [AccountBody]):
    account_list = unique_basemodel_list(accounts, "account_id")
    insert_statement = postgresql.insert(Account).values(account_list)
    upsert_statement = insert_statement.on_conflict_do_nothing(
        index_elements=["account_id"],
    )
    with get_session() as session:
        session.execute(upsert_statement)
        session.commit()


def upsert_member_accounts(member_accounts: [MemberAccountBody]) -> None:
    member_account_list = unique_basemodel_list(member_accounts, "client_member_id")
    values = __get_upsert_member_ids(member_account_list)
    insert_statement = postgresql.insert(MemberAccount).values(values)
    update_columns = {
        col.name: col
        for col in insert_statement.excluded
        if col.name not in ["member_id"]
    }
    upsert_statement = insert_statement.on_conflict_do_update(
        index_elements=["member_id"], set_=update_columns
    )
    with get_session() as session:
        session.execute(upsert_statement)
        session.commit()


def __get_upsert_member_ids(member_account_list: [MemberAccountBody]):
    client_member_ids = list(
        map(lambda item: item["client_member_id"], member_account_list)
    )
    select_statement: Select = sa.select(
        [Member.member_id, Member.client_member_id],
        Member.client_member_id.in_(client_member_ids),
    )
    parsed_results = {}
    with get_session() as session:
        result: Result = session.execute(select_statement)
        for row in result.all():
            parsed_results[row[1]] = {"member_id": row[0]}

    return list(
        map(
            lambda item: {
                "account_id": item["account_id"],
                "member_id": parsed_results[item["client_member_id"]]["member_id"],
            },
            member_account_list,
        )
    )
