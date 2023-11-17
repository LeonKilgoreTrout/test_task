import pytest
from app.database import session
import asyncio
from insert_templates import insert


@pytest.fixture(scope="session")
def event_loop():

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    loop.run_until_complete(insert())
    yield loop
    session.drop()
    loop.close()


