from sqlalchemy.orm import Session

from src.account.models import Account, AccountBody
from src.account.queries_db import upsert_accounts


def cleanup(db_session):
    db_session.query(Account).delete()


def test_upsert_accounts(db_session: Session):
    result = db_session.query(Account).all()
    assert len(result) == 0
    upsert_accounts([
        AccountBody(account_id=2),
        AccountBody(account_id=3)
    ])
    result = db_session.query(Account).all()
    assert len(result) == 2
    cleanup(db_session)


def test_upsert_accounts_handles_duplicates(db_session: Session):
    upsert_accounts([
        AccountBody(account_id=2),
        AccountBody(account_id=2),
        AccountBody(account_id=3)
    ])
    result = db_session.query(Account).all()
    assert len(result) == 2
