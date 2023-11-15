import motor.motor_asyncio
from motor.core import AgnosticClient

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

loop = client.get_io_loop()


class Session:

    def __init__(self, client: AgnosticClient):
        self.loop = client.get_io_loop()
        self.collection = client.forms.templates

    async def _do_insert(self, form):
        await self.collection.insert_one(form)

    async def _find_one(self, form):
        print(form)
        print({
                key: {"$eq": value} for key, value in form.items()
            })
        result = await self.collection.find_one(
            {
                key: {"$eq": value} for key, value in form.items()
            }
        )
        print(result)
        return result if result else None

    def do_insert(self, dict_):
        self.loop.run_until_complete(self._do_insert(dict_))

    def find_one(self, f):
        return self.loop.run_until_complete(self._find_one(f))


session = Session(client=client)
