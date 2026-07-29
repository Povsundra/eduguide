from typing import Callable, Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

RepositoryType = TypeVar("RepositoryType")

def get_repository(repo_type: Type[RepositoryType]) -> Callable[..., RepositoryType]:
    """
    Dependency factory to inject a repository instance with a database session.
    
    Usage:
        def some_route(user_repo: CRUDUser = Depends(get_repository(CRUDUser))):
            ...
    """
    def _get_repo(db: AsyncSession = Depends(get_db)) -> RepositoryType:
        return repo_type(db)
        
    return _get_repo
