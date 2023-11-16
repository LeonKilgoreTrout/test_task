from logger import log
import motor.motor_asyncio
from motor.core import AgnosticClient
from settings import settings
from typing import Dict


class Session:

    def __init__(self, client: AgnosticClient):
        self.loop = client.get_io_loop()
        self.collection = client.forms.templates

    async def _do_insert(self, template: Dict) -> None:
        await self.collection.insert_one(template)
        log("Template added to `templates` collection", added=template)

    async def _find_one(self, template: Dict) -> Dict | None:
        result = await self.collection.find_one(template)
        if result is None:
            log("Template not found in `templates` collection")
        else:
            log("Template found in `templates` collection", found=result)
        return result


client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo.DATABASE_URL)
session = Session(client=client)
