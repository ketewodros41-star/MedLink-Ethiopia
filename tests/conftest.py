import os
import sys
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_medlink.db"
os.environ["AUTO_CREATE_TABLES"] = "true"
os.environ["MEILI_ENABLED"] = "false"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.deps import get_current_user
from app.core.security import verify_medplum_token
from app.db.base import Base
from app.db.redis import get_redis
from app.db.session import AsyncSessionLocal, engine, get_db
from app.main import app
from app.core.metrics import metrics_registry


class FakeRedis:
    def __init__(self) -> None:
        self.messages: list[tuple[str, dict]] = []

    async def xadd(self, stream: str, payload: dict):
        self.messages.append((stream, payload))
        return "1-0"


@pytest_asyncio.fixture(autouse=True)
async def reset_db() -> AsyncIterator[None]:
    metrics_registry.counters.clear()
    metrics_registry.latency_totals_ms.clear()
    metrics_registry.latency_counts.clear()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    fake_redis = FakeRedis()
    user_context = {"sub": "user-123", "roles": ["patient"]}

    async def override_db():
        yield db_session

    async def override_user():
        return user_context

    async def override_token():
        return user_context

    async def override_redis():
        return fake_redis

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[verify_medplum_token] = override_token
    app.dependency_overrides[get_redis] = override_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        test_client.user_context = user_context
        yield test_client

    app.dependency_overrides.clear()
    await db_session.rollback()
