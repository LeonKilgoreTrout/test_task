from app.main import app
from httpx import AsyncClient
import pytest


"""
    В данном наборе тестов не обязательно выполнять подключение к Mongo, 
    (вообще оно происходит, но нет предварительного добавления/удаления данных 
    т к необходимо проверить выполняется ли определение типов, когда подходящих шаблонов нет
"""

PSEUDO_URL = "http://test"


@pytest.mark.asyncio
async def test_random():
    case = "test_field=qwdq"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "text"}


@pytest.mark.asyncio
async def test_phone_field():
    case = "test_field=+79098083789"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "phone"}


@pytest.mark.asyncio
async def test_email_field():
    case = "test_field=test@test.st"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "email"}


@pytest.mark.asyncio
async def test_date1_field():
    case = "test_field=2021-09-29"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "date"}


@pytest.mark.asyncio
async def test_date2_field():
    case = "test_field=31.12.1998"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {"test_field": "date"}


@pytest.mark.asyncio
async def test_few_fields():
    case = "test_field=31.12.1998&test_field_2=+79098083789"
    async with AsyncClient(app=app, base_url=PSEUDO_URL) as ac:
        response = await ac.post(f"/api/get_form/{case}")
        assert response.json() == {'test_field': 'date', 'test_field_2': 'phone'}
