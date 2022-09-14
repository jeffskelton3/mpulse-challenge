import asyncio
import json
import os

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from src.account.models import AccountBody, MemberAccountBody
from src.account.queries_db import upsert_accounts, upsert_member_accounts
from src.member.models import MemberBody
from src.member.queries_db import upsert_members

KAFKA_INSTANCE = os.getenv("KAFKA_URL", "")
CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "")
loop = asyncio.get_event_loop()


class BulkMemberIngestion:
    def __init__(self,
                 producer=AIOKafkaProducer(bootstrap_servers=KAFKA_INSTANCE, client_id=CLIENT_ID, loop=loop),
                 consumer=AIOKafkaConsumer("member_upload", bootstrap_servers=KAFKA_INSTANCE, client_id=CLIENT_ID,
                                           loop=loop)):
        self.producer = producer
        self.consumer = consumer

    async def consume(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                csv_rows = json.loads(msg.value.decode("utf-8"))
                members = list(map(lambda item: MemberBody(**item), csv_rows))
                accounts = list(map(lambda item: AccountBody(**item), csv_rows))
                member_accounts = list(
                    map(lambda item: MemberAccountBody(**item), csv_rows)
                )
                upsert_accounts(accounts)
                upsert_members(members)
                upsert_member_accounts(member_accounts)
        finally:
            await self.consumer.stop()

    async def ingest(self, data: bytes):
        await self.producer.send("member_upload", data)
