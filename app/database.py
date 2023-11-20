from functools import lru_cache
from logger import log
import motor.motor_asyncio
from motor.core import AgnosticClient
from settings import settings
from typing import Dict, List
from collections import Counter


DATABASE_URL = settings.mongo.DATABASE_URL
MAX_POSSIBLE_TEMPLATES = settings.MAX_POSSIBLE_TEMPLATES


def _find_max(lst: List[str]):
    frequency_dict = Counter(lst)
    if len(frequency_dict):
        max_amount = max(frequency_dict.values())
        form_names = \
            [form_name for form_name, amount in frequency_dict.items() if amount == max_amount]
        return form_names
    return None


@lru_cache
class Session:

    def __init__(self, client: AgnosticClient, collection: str):
        self.collection_name = collection
        self.collection = client.forms[f"{collection}"]

    def drop(self):
        self.collection.delete_many({})
        log(f"Collection `{self.collection_name}` has been cleared")

    async def do_insert(self, form: Dict) -> None:
        await self.collection.insert_one(form)
        log(f"Template added to `{self.collection_name}` collection", added=form)

    async def find_all(self, template: Dict) -> Dict | None:
        match_list = []
        for field_, type_or_name in template.items():
            if field_ != "name":
                results = self.collection.find({field_: {'$regex': type_or_name}})
                for form in await results.to_list(length=MAX_POSSIBLE_TEMPLATES):
                    match_list += [form["name"]]
        if len(match_list):
            log(f"Templates found in `{self.collection_name}` collection")
        else:
            log(f"Templates not found in `{self.collection_name}` collection")
        return _find_max(match_list)


session = Session(
    client=motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL),
    collection="templates"
)
