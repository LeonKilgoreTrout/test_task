from app.database import session
import asyncio


templates = [
    {
        "field_1": "email",
        "field_2": "phone",
        "field_3": "text",
        "field_4": "date",
        "field_5": "date"
    },
    {
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
