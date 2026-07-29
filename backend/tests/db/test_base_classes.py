import asyncio
import uuid
from datetime import datetime
import pytest
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.base_class import Base
from app.db.mixins import UUIDMixin, TimestampMixin

class DummyModel(Base, UUIDMixin, TimestampMixin):
    name: Mapped[str] = mapped_column(String(50))

import pytest_asyncio

@pytest.mark.asyncio
async def test_table_name_generation():
    assert DummyModel.__tablename__ == "dummy_model"

@pytest.mark.asyncio
async def test_uuid_mixin(db_session: AsyncSession):
    dummy = DummyModel(name="uuid_test")
    db_session.add(dummy)
    await db_session.commit()
    await db_session.refresh(dummy)
    
    assert dummy.id is not None
    assert isinstance(dummy.id, uuid.UUID)

@pytest.mark.asyncio
async def test_timestamp_mixin(db_session: AsyncSession):
    dummy = DummyModel(name="timestamp_test")
    db_session.add(dummy)
    await db_session.commit()
    
    assert dummy.created_at is not None
    assert dummy.updated_at is not None
    
    initial_updated = dummy.updated_at
    initial_created = dummy.created_at
    
    # Wait to ensure timestamp change
    await asyncio.sleep(0.01)
    
    # Trigger update
    dummy.name = "updated"
    await db_session.commit()
    await db_session.refresh(dummy)
    
    assert dummy.updated_at.replace(tzinfo=None) > initial_updated.replace(tzinfo=None)
    assert dummy.created_at.replace(tzinfo=None) == initial_created.replace(tzinfo=None)
