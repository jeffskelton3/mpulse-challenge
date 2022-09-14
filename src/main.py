import codecs
import csv

from fastapi import FastAPI, UploadFile, File

from src.account.models import MemberAccountBody, AccountBody
from src.account.queries_db import upsert_member_accounts, upsert_accounts, find_by_account_id
from src.member.models import MemberBody, CreateMemberBody
from src.member.queries_db import get_members, upsert_members, find_by_id

app = FastAPI()


@app.get("/members")
async def member_search(limit=20, offset=0, phone_number=None, client_member_id=None):
    return get_members({
        "phone_number": phone_number,
        "client_member_id": client_member_id,
        "limit": limit,
        "offset": offset
    })


@app.get("/members/{member_id}")
async def find_member_by_id(member_id: str):
    return find_by_id(member_id)


@app.get("/accounts/{account_id}/members")
async def find_member_by_account(account_id: int):
    return find_by_account_id(account_id)


@app.post("/members/upload")
def upload(file: UploadFile = File(...)):
    csv_rows = list(csv.DictReader(codecs.iterdecode(file.file, 'utf-8')))
    members = list(map(lambda item: MemberBody(**item), csv_rows))
    accounts = list(map(lambda item: AccountBody(**item), csv_rows))
    member_accounts = list(map(lambda item: MemberAccountBody(**item), csv_rows))
    upsert_accounts(accounts)
    upsert_members(members)
    upsert_member_accounts(member_accounts)


@app.post("/members")
async def create_member(body: CreateMemberBody):
    payload = body.dict()
    upsert_accounts([AccountBody(**payload)])
    upsert_members([MemberBody(**payload)])
    upsert_member_accounts([MemberAccountBody(**payload)])
