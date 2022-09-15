from src.member.models import MemberBody
from src.member.queries_db import get_members, upsert_members


def test_returns_members(db_session):
    upsert_members([MemberBody(
        client_member_id="123",
        first_name="Jeff",
        last_name="Lebowski",
        phone_number="5555555555"
    )])
    results = get_members()
    print(results)
    assert results == []
