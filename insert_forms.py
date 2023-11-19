from app.database import session
import asyncio
import uuid


def _gen_name() -> str:
    return str(uuid.uuid4())


forms = [
    {
        "name": _gen_name(),
        "field_1": "email",
        "field_2": "phone",
        "field_3": "text",
        "field_4": "date",
        "field_5": "date"
    },
    {
        "name": _gen_name(),
        "foo": "phone",
        "bar": "text"
    },
    {
        "name": _gen_name(),
        "owner_email": "email",
        "customer_phone": "phone"
    },
    {
        "name": _gen_name(),
        "owner_email": "email",
        "order_date": "date"
    }
]


async def insert():
    for form in forms:
        await session.do_insert(form)


if __name__ == "__main__":
    asyncio.run(insert())
    print("Done!!!")
    exit()
