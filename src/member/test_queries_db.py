from src.member.models import MemberBody, Member
from src.member.queries_db import get_members, upsert_members, find_by_id

members_stub = [
    MemberBody(
        client_member_id="123",
        first_name="Jeff",
        last_name="Lebowski",
        phone_number="5555555555",
    ),
    MemberBody(
        client_member_id="456",
        first_name="Walter",
        last_name="Solcheck",
        phone_number="4444444444",
    ),
]


def test_returns_members():
    upsert_members(members_stub)
    results = get_members()
    for i, result in enumerate(results):
        assert result.client_member_id == members_stub[i].client_member_id
        assert result.first_name == members_stub[i].first_name
        assert result.last_name == members_stub[i].last_name
        assert result.phone_number == members_stub[i].phone_number


def test_phone_filter():
    upsert_members(members_stub)
    results = get_members({"phone_number": "5555555555"})
    assert len(results) == 1
    assert results[0].phone_number == "5555555555"


def test_client_id_filter():
    upsert_members(members_stub)
    results = get_members({"client_member_id": "456"})
    assert len(results) == 1
    assert results[0].client_member_id == "456"


def test_pagination():
    upsert_members(members_stub)
    results = get_members({"size": "1", "page": "1"})
    assert len(results) == 1


def test_find_by_member_id(db_session):
    member = Member(
        first_name="Donny",
        last_name="Kerabatsos",
        phone_number="3333333333",
        client_member_id="789",
    )
    db_session.add(member)
    db_session.commit()
    created_record = db_session.query(Member).first()
    result = find_by_id(str(created_record.member_id))
    assert result.member_id == created_record.member_id
