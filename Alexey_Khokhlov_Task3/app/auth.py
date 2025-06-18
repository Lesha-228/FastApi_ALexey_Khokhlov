from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from .models import User
from .schemas import UserCreate, UserLogin, UserRead
from .database import get_session
from .security import get_password_hash, verify_password

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")


    new_user = User(username=user.username, password=get_password_hash(user.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()


    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}