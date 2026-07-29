import pytest
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.crud.base import CRUDBase
from app.api.deps import get_repository
from app.models.user import User
from app.db.base_class import Base

# Dummy Pydantic schemas
class DummyCreate(BaseModel):
    email: str
    is_active: bool = True

class DummyUpdate(BaseModel):
    email: str | None = None
    is_active: bool | None = None

class CRUDDummy(CRUDBase[User, DummyCreate, DummyUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

import pytest_asyncio

@pytest.mark.asyncio
async def test_crud_base_operations(db_session: AsyncSession):
    repo = CRUDDummy(db_session)
    
    # 1. Create
    obj_in = DummyCreate(email="crud@example.com")
    db_obj = await repo.create(obj_in=obj_in)
    
    assert db_obj.id is not None
    assert db_obj.email == "crud@example.com"
    
    # 2. Get
    fetched = await repo.get(id=db_obj.id)
    assert fetched is not None
    assert fetched.email == "crud@example.com"
    
    # 3. Get Multi
    multi = await repo.get_multi()
    assert len(multi) == 1
    
    # 4. Update
    update_in = DummyUpdate(email="updated@example.com")
    updated = await repo.update(db_obj=fetched, obj_in=update_in)
    assert updated.email == "updated@example.com"
    
    # 5. Remove
    removed = await repo.remove(id=db_obj.id)
    assert removed.email == "updated@example.com"
    
    empty = await repo.get(id=db_obj.id)
    assert empty is None

@pytest.mark.asyncio
async def test_dependency_injection():
    # Verify the DI factory compiles and returns a callable function
    dep_func = get_repository(CRUDDummy)
    assert callable(dep_func)
