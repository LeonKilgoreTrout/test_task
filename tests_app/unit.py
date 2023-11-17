from app.main import app
from httpx import AsyncClient
import pytest
from app.database import session


PSEUDO_URL = "http://test"


@pytest.mark.asyncio
async def test_random(event_loop):
    case = "test_field=qwdq"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "text"}


@pytest.mark.asyncio
async def test_phone_field(event_loop):
    case = "test_field=+79098083789"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "phone"}


@pytest.mark.asyncio
async def test_email_field(event_loop):
    case = "test_field=test@test.st"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "email"}


@pytest.mark.asyncio
async def test_date1_field(event_loop):
    case = "test_field=2021-09-29"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "date"}


@pytest.mark.asyncio
async def test_date2_field(event_loop):
    case = "test_field=31.12.1998"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "date"}


@pytest.mark.asyncio
async def test_few_fields(event_loop):
    case = "test_field=31.12.1998&test_field_2=+79098083789"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {'test_field': 'date', 'test_field_2': 'phone'}


@pytest.mark.asyncio
async def test_match(event_loop):
    case = "field_1=some@mail.com&field_2=+7 923 098 9023&field_3=Hello, world!&field_4=31.12.1998&field_5=2021-09-29"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        # cursor = session.collection.find({})
        # async for document in cursor:
        #     print("3123")
        #     print(document)
        # # print()
        # print("++++++++++++++++++++")
        # print(response.json())

        assert len(response.json()) == 1
