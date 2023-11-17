from functools import lru_cache
from logger import log
import motor.motor_asyncio
from motor.core import AgnosticClient
from settings import settings
from typing import Dict


@lru_cache
class Session:

    def __init__(self, client: AgnosticClient, collection: str):
        self.collection_name = collection
        self.collection = client.forms[f"{collection}"]

    def drop(self):
        self.collection.delete_many({})

    async def _do_insert(self, template: Dict) -> None:
        await self.collection.insert_one(template)
        log(f"Template added to `{self.collection_name}` collection", added=template)

    async def _find_one(self, template: Dict) -> Dict | None:
        result = await self.collection.find_one(template)
        if result is None:
            log(f"Template not found in `{self.collection_name}` collection")
        else:
            log(f"Template found in `{self.collection_name}` collection", found=result)
        return result


session = Session(
    client=motor.motor_asyncio.AsyncIOMotorClient(settings.mongo.DATABASE_URL),
    collection="templates"
)
