from app.main import app
from httpx import AsyncClient
import pytest

PSEUDO_URL = "http://test"


@pytest.mark.asyncio
async def test_full_match(event_loop):
    case = "field_1=some@mail.com&field_2=+7 923 098 9023&field_3=Hello, world!&field_4=31.12.1998&field_5=2021-09-29"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        rdict = response.json()
        assert len(rdict) == 1
        assert "template_names" in rdict.keys()


@pytest.mark.asyncio
async def test_match_less_fields(event_loop):
    case = "field_1=some@mail.com&field_3=Hello, world!&field_4=31.12.1998&field_5=2021-09-29"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        rdict = response.json()
        assert len(rdict) == 1
        assert "template_names" in rdict.keys()


@pytest.mark.asyncio
async def test_match_extra_fields(event_loop):
    case = "field_1=some@mail.com&test_field=31.12.1998&test_field_2=+79098083789&" \
           "field_3=Hello, world!&field_4=31.12.1998&field_5=2021-09-29"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        rdict = response.json()
        assert len(rdict) == 1
        assert "template_names" in rdict.keys()


@pytest.mark.asyncio
async def test_match_two_forms(event_loop):
    case = "owner_email=some@mail.ru&customer_phone=+79437684343&order_date=31.12.1998"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        rdict = response.json()
        assert len(rdict) == 1
        assert "template_names" in rdict.keys()
        assert len(rdict["template_names"]) == 2
