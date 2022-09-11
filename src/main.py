import codecs
import csv

from fastapi import FastAPI, UploadFile, File

from src.account.models import MemberAccountBody, AccountBody
from src.account.queries_db import upsert_member_accounts, upsert_accounts, find_by_account_id
from src.member.models import MemberBody
from src.member.queries_db import get_members, add_member, upsert_members, find_member_by_client_member_id, find_by_id, \
    find_by_phone_number

app = FastAPI()


@app.get("/client/members/{client_member_id}")
async def find_member_by_id(client_member_id: str):
    """
    Get a member by their client_member_id
    :return: Member
    """
    return find_member_by_client_member_id(client_member_id)


@app.get("/members/{member_id}")
async def find_member_by_id(member_id: str):
    """
    Get a member by their ID
    :return: Member
    """
    return find_by_id(member_id)


@app.get("/accounts/{account_id}/members")
async def find_member_by_account(account_id: int):
    """
    Get a members for a given Account ID
    :return:
    """
    return find_by_account_id(account_id)


@app.get("/members/phone/{phone_number}")
async def find_member_by_phone(phone_number: str):
    """
    Get a member by their Phone Number
    """
    return find_by_phone_number(phone_number)


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
async def create_member(member: MemberBody):
    """
    Create a new Member
    """
    return add_member(member)
