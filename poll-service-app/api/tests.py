import pytest_asyncio

from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import main_app, lifespan
from core.models import db_helper, Poll, Option, Vote
from core.config import settings
from core.models.base import Base


engine = create_async_engine(
    url=str(settings.dbtest.url),
    poolclass=NullPool,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        yield session


async def override_lifespan(app: FastAPI):
    yield
    await engine.dispose()


main_app.dependency_overrides[db_helper.session_getter] = get_async_session
main_app.dependency_overrides[lifespan] = override_lifespan


@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    ) as ac:
        yield ac


async def test_get_polls(ac: AsyncClient):
    poll = Poll(title="title", description="description")
    options = [Option(point=point) for point in ["yes", "no"]]
    poll.options = options
    async with async_session() as session:
        session.add(poll)
        await session.commit()
    response = await ac.get("/api/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "title",
            "description": "description",
            "id": 1,
            "options": [
                {"point": "yes", "poll_id": 1, "id": 1},
                {"point": "no", "poll_id": 1, "id": 2},
            ],
        }
    ]


async def test_create_poll(ac: AsyncClient):
    request_body = {
        "title": "title",
        "description": "description",
        "options": [{"point": "yes"}],
    }
    response = await ac.post("/api/create-poll/", json=request_body)
    assert response.status_code == 200
    assert response.json() == {
        "title": "title",
        "description": "description",
        "id": 1,
        "options": [{"point": "yes"}],
    }


async def test_submit_vote(ac: AsyncClient):
    poll = Poll(title="title", description="description")
    options = [Option(point=point) for point in ["yes", "no"]]
    poll.options = options
    async with async_session() as session:
        session.add(poll)
        await session.commit()
    request_body = {"poll_id": 1, "choice_id": 1}
    response = await ac.post("/api/poll/", json=request_body)
    async with async_session() as session:
        option = await session.get(Vote, 1)
    assert response.status_code == 200
    assert option.poll_id == 1
    assert option.choice_id == 1


async def test_get_result(ac: AsyncClient):
    poll = Poll(title="title", description="description")
    options = [Option(point=point) for point in ["yes", "no"]]
    poll.options = options
    async with async_session() as session:
        session.add(poll)
        await session.commit()
    vote_1 = Vote(poll_id=1, choice_id=1)
    vote_2 = Vote(poll_id=1, choice_id=1)
    async with async_session() as session:
        session.add_all([vote_1, vote_2])
        await session.commit()
    response = await ac.get("/api/get-result/1")
    assert response.status_code == 200
    assert response.json() == {
        "poll_id": 1,
        "result": [
            {"option_id": 1, "vote_count": 2},
            {"option_id": 2, "vote_count": 0},
        ],
    }
