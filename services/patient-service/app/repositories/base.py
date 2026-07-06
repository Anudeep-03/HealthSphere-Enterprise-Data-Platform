from typing import Generic, TypeVar, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound="Base")

class BaseRepository(Generic[T]):
    """
    Abstract base repository providing common CRUD operations.
    """
    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: Any) -> Optional[T]:
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def list(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj_in: Any) -> T:
        # Note: obj_in should be an ORM model instance
        self.session.add(obj_in)
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    async def delete(self, id: Any) -> bool:
        obj = await self.get(id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
