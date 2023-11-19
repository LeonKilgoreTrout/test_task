import pytest
from app.database import session
import asyncio
from insert_forms import insert


@pytest.fixture(scope="session")
def event_loop():
    """ Помимо объявления нового цикла для каждого теста, также наполняем и дропаем БД """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(insert())
    yield loop
    session.drop()
    loop.close()


