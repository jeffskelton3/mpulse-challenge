import codecs
import csv

from fastapi import FastAPI, UploadFile, File

from src.member.models import MemberBody
from src.member.queries_db import get_members, add_member, upsert_members, find_member_by_client_member_id, find_by_id

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


@app.get("account/{account_id}/members")
async def find_member_by_account():
    """
    Get a member for a given Account ID
    :return:
    """
    return {"message": "Hello World"}


@app.get("/members")
async def member_search():
    """
    Get a member by their Phone Number
    Get a member by their Client Member ID
    """
    return get_members()


@app.post("/members/upload")
def upload(file: UploadFile = File(...)):
    member_list = list(csv.DictReader(codecs.iterdecode(file.file, 'utf-8')))
    members = list(map(lambda item: MemberBody(**item), member_list))
    return upsert_members(members)
    # return get_members()


@app.post("/members")
async def create_member(member: MemberBody):
    """
    Create a new Member
    """
    return add_member(member)
