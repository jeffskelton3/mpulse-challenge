import codecs
import asyncio
import csv
import json

from fastapi import FastAPI, UploadFile, File

from src.account.models import MemberAccountBody, AccountBody
from src.account.queries_db import (
    upsert_member_accounts,
    upsert_accounts,
    find_by_account_id,
)
from src.ingestion.bulk_member_ingestion import BulkMemberIngestion
from src.member.models import MemberBody, CreateMemberBody
from src.member.queries_db import get_members, upsert_members, find_by_id

app = FastAPI()

loop = asyncio.get_event_loop()
bulk_member_ingestion_client = BulkMemberIngestion()


@app.on_event("startup")
async def startup_event():
    await bulk_member_ingestion_client.producer.start()
    loop.create_task(bulk_member_ingestion_client.consume())


@app.on_event("shutdown")
async def shutdown_event():
    await bulk_member_ingestion_client.producer.stop()


@app.get("/members")
async def member_search(size=20, page=1, phone_number=None, client_member_id=None):
    return get_members({
        "phone_number": phone_number,
        "client_member_id": client_member_id,
        "size": size,
        "page": page,
    })


@app.get("/members/{member_id}")
async def find_member_by_id(member_id: str):
    return find_by_id(member_id)


@app.get("/accounts/{account_id}/members")
async def find_member_by_account(account_id: int):
    return find_by_account_id(account_id)


@app.post("/members/upload")
async def upload(file: UploadFile = File(...)):
    csv_rows = json.dumps(
        list(csv.DictReader(codecs.iterdecode(file.file, "utf-8")))
    ).encode("ascii")
    await bulk_member_ingestion_client.ingest(csv_rows)


@app.post("/members")
async def create_member(body: CreateMemberBody):
    payload = body.dict()
    upsert_accounts([AccountBody(**payload)])
    upsert_members([MemberBody(**payload)])
    upsert_member_accounts([MemberAccountBody(**payload)])
