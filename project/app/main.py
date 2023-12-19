from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session, init_db
from app.models import User,UserCreate, Event, EventCreate, UserEventLink, UserId

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/user", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    
    return [User(name=user.name, user_name=user.user_name, email=user.email, id=user.id) for user in users]


@app.get("/user/{id}", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    
    return [User(name=user.name, user_name=user.user_name, email=user.email, id=user.id) for user in users]



@app.post("/user")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(name=user.name, user_name=user.user_name, email=user.email)
 
    session.add(user)
    
    await session.commit()
    await session.refresh(user)
    
    return user

@app.put("/user")
async def add_user(user: User, session: AsyncSession = Depends(get_session)):
    user = User(name=user.name, user_name=user.user_name, email=user.email)
    session.add(user)
    
    await session.commit()
    await session.refresh(user)
    
    return user

@app.get("/event", response_model=list[Event])
async def get_events(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Event))
    events = result.scalars().all()
    
    return [Event(name=event.name, description=event.description, id=event.id) for event in events]


@app.get("/event/{id}", response_model=list[Event])
async def get_event(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Event).where(Event.id == id))
    events = result.scalars().all()
    
    return [Event(name=event.name, description=event.description, id=event.id) for event in events]


@app.post("/event")
async def add_event(event: EventCreate, session: AsyncSession = Depends(get_session)):
    event = Event(name=event.name, description=event.description)
 
    session.add(event)
    
    await session.commit()
    await session.refresh(event)
    
    return event

@app.post("/event/{id}")
async def add_event(id: int, user: UserId, session: AsyncSession = Depends(get_session)):
    event_user = UserEventLink(user_id=user.id, event_id=id)
 
    session.add(event_user)
    
    await session.commit()
    await session.refresh(event_user)
    
    return event_user
