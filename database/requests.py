from sqlalchemy import delete, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from aiogram_dialog import DialogManager

from database import models


async def add_user(session: AsyncSession, telegram_id: int, username: str | None):
    stmt = (
        pg_insert(models.User)
        .values(telegram_id=telegram_id, username=username)
        .on_conflict_do_update(
            index_elements=[models.User.telegram_id],
            set_={'username': username}
        )
    )


async def get_material_by_group(session: AsyncSession, group: int):
    stmt = select(models.Material).where(models.Material.group == group)

    result = await session.execute(stmt)

    return result.scalars().all()


async def get_photo_by_group(session: AsyncSession, group: int):
    stmt = select(models.Material.menu_photo_path).where(models.Material.group == group)
    result = await session.execute(stmt)

    photo=result.first()
    return photo[0] if photo else None


async def get_photo_by_material_id(session: AsyncSession, material_id: int):
    stmt = select(models.Material.brick_photo_path).where(models.Material.id == material_id)

    result = await session.execute(stmt)

    return result.scalar()



async def get_material_name(session: AsyncSession, material_id: int):
    stmt = (
        select(models.Material.name)
        .where(models.Material.id == material_id)
    )

    result = await session.execute(stmt)

    return result.scalar()