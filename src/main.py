import codecs
import asyncio
import csv
import json
import uuid

from fastapi import FastAPI, UploadFile, File
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, AIOKafkaClient
from pydantic import BaseModel, StrictStr

from src.account.models import MemberAccountBody, AccountBody
from src.account.queries_db import upsert_member_accounts, upsert_accounts, find_by_account_id
from src.member.models import MemberBody, CreateMemberBody
from src.member.queries_db import get_members, upsert_members, find_by_id

app = FastAPI()

loop = asyncio.get_event_loop()
KAFKA_INSTANCE = "kafka:9092"
PROJECT_NAME = "mpulse-challenge-kafka"
producer = AIOKafkaProducer(bootstrap_servers=KAFKA_INSTANCE, client_id=PROJECT_NAME, loop=loop)
client = AIOKafkaClient(bootstrap_servers=KAFKA_INSTANCE)


class ProducerResponse(BaseModel):
    name: StrictStr
    message_id: StrictStr
    topic: str
    timestamp: StrictStr = ""


class ProducerMessage(BaseModel):
    name: StrictStr
    message_id: StrictStr = ""
    timestamp: StrictStr = ""


@app.on_event("startup")
async def startup_event():
    await producer.start()
    loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()


@app.get("/members")
async def member_search(size=20, page=1, phone_number=None, client_member_id=None):
    return get_members({
        "phone_number": phone_number,
        "client_member_id": client_member_id,
        "size": size,
        "page": page
    })


@app.get("/members/{member_id}")
async def find_member_by_id(member_id: str):
    return find_by_id(member_id)


@app.get("/accounts/{account_id}/members")
async def find_member_by_account(account_id: int):
    return find_by_account_id(account_id)


@app.post("/members/upload")
async def upload(file: UploadFile = File(...)):
    csv_rows = json.dumps(list(csv.DictReader(codecs.iterdecode(file.file, 'utf-8')))).encode("ascii")
    await producer.send("member_upload", csv_rows)


@app.post("/members")
async def create_member(body: CreateMemberBody):
    payload = body.dict()
    upsert_accounts([AccountBody(**payload)])
    upsert_members([MemberBody(**payload)])
    upsert_member_accounts([MemberAccountBody(**payload)])


async def consume():
    consumer = AIOKafkaConsumer("member_upload", bootstrap_servers=KAFKA_INSTANCE, client_id=PROJECT_NAME, loop=loop)
    await consumer.start()
    try:
        async for msg in consumer:
            csv_rows = json.loads(msg.value.decode("utf-8"))
            members = list(map(lambda item: MemberBody(**item), csv_rows))
            accounts = list(map(lambda item: AccountBody(**item), csv_rows))
            member_accounts = list(map(lambda item: MemberAccountBody(**item), csv_rows))
            upsert_accounts(accounts)
            upsert_members(members)
            upsert_member_accounts(member_accounts)
    finally:
        await consumer.stop()
