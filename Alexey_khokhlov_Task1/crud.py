from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models import Note

async def create_note(session: AsyncSession, text: str) -> Note:
    note = Note(text=text)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note

async def get_notes(session: AsyncSession) -> list[Note]:
    result = await session.execute(select(Note))
    return result.scalars().all()
