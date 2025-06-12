from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Note
from schemas import NoteCreate, NoteOut
from database import get_session, engine, SQLModel

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)



@app.post("/notes", response_model=NoteOut)
async def create_note(
    note: NoteCreate,
    session: AsyncSession = Depends(get_session)
):
    new_note = Note(text=note.text)
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note



@app.get("/notes", response_model=list[NoteOut])
async def get_notes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note))
    notes = result.scalars().all()
    return notes

