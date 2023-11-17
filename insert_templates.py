from app.database import session
import asyncio
import uuid


templates = [
    {
        "name": str(uuid.uuid4()),
        "field_1": "email",
        "field_2": "phone",
        "field_3": "text",
        "field_4": "date",
        "field_5": "date"
    },
    {
        "name": str(uuid.uuid4()),
        "foo": "phone",
        "bar": "text"
    }
]


async def insert():
    for template in templates:
        await session._do_insert(template)


if __name__ == "__main__":
    asyncio.run(insert())
    exit()
